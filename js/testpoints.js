/*
 * testpoints.js — what a test point should read, and whether a reading is good.
 *
 * The expectation for a point comes in one of five printed forms, and the
 * evaluator has to handle all of them because the manuals mix them freely:
 *
 *   nominal + tolerance      absolute volts,  "TP5 ... 33.0 V +/-0.5 V"
 *   nominal + tolerancePct   percentage,      "TP209 ... +565 +/-10%"
 *   maxAbs                   a ceiling on |v|, "TP201 ... less than 1.0V"
 *   min / max                one-sided limits, "TP3 ... 60 V dc or less",
 *                            "EXT PWR ... 24 V dc minimum"
 *   min + max                a window with no stated centre, "24.5 to 26.5 V"
 *
 * Rails that are only a return path carry no expectation at all, and a point
 * may carry a list of states when its correct reading depends on which mode
 * the circuit has been put into.
 */
(function (global) {
  'use strict';

  var TestPoints = {};

  /** The expectation objects a point offers: either its states, or itself. */
  TestPoints.states = function (tp) {
    if (!tp) return [];
    if (tp.states && tp.states.length) return tp.states;
    if (tp.isReturn) return [];
    if (tp.nominal == null && tp.maxAbs == null && tp.min == null && tp.max == null) return [];
    return [{
      label: tp.condition || 'Nominal',
      nominal: tp.nominal,
      tolerance: tp.tolerance,
      tolerancePct: tp.tolerancePct,
      maxAbs: tp.maxAbs,
      min: tp.min,
      max: tp.max,
      source: tp.source,
      onFail: tp.onFail
    }];
  };

  TestPoints.hasExpectation = function (tp) {
    return TestPoints.states(tp).length > 0;
  };

  /**
   * Absolute limits for one state, or null when it has no expectation.
   *
   * `lo`/`hi` are the accept limits, with -Infinity / Infinity standing for
   * the open side of a one-sided limit. `nominal` is the midpoint of a
   * two-sided window and the bound itself for a one-sided one -- the manual
   * states no centre for "60 V or less", so the bound is the only number
   * there is to measure a deviation from. `tol` is half the window for
   * min+max and 5% of the bound for a one-sided limit: that is the width of
   * the "near the limit" band, not a published tolerance.
   */
  TestPoints.range = function (state) {
    if (!state) return null;
    if (state.maxAbs != null) {
      var base = state.nominal == null ? 0 : state.nominal;
      return { lo: base - state.maxAbs, hi: base + state.maxAbs, nominal: base,
               tol: state.maxAbs, kind: 'maxAbs' };
    }
    // Coerced, as the nominal path coerces through its arithmetic: a bound
    // that arrives as the string "24" from a hand-edited file must not reach
    // fmt() as something without toFixed.
    var hasMin = state.min != null && state.min !== '' && !isNaN(state.min);
    var hasMax = state.max != null && state.max !== '' && !isNaN(state.max);
    if (hasMin && hasMax) {
      var lo = Math.min(+state.min, +state.max), hi = Math.max(+state.min, +state.max);
      return { lo: lo, hi: hi, nominal: (lo + hi) / 2, tol: (hi - lo) / 2, kind: 'minmax' };
    }
    if (hasMin) {
      return { lo: +state.min, hi: Infinity, nominal: +state.min,
               tol: Math.abs(+state.min) * 0.05, kind: 'min' };
    }
    if (hasMax) {
      return { lo: -Infinity, hi: +state.max, nominal: +state.max,
               tol: Math.abs(+state.max) * 0.05, kind: 'max' };
    }
    if (state.nominal == null) return null;
    var tol = state.tolerance;
    if (tol == null && state.tolerancePct != null) {
      tol = Math.abs(state.nominal) * state.tolerancePct / 100;
    }
    if (tol == null) return null;
    return { lo: state.nominal - tol, hi: state.nominal + tol,
             nominal: state.nominal, tol: tol,
             kind: state.tolerancePct != null ? 'pct' : 'abs' };
  };

  /**
   * Score a measurement.
   *
   * Green inside the inner half of the tolerance band, amber in the outer half,
   * red outside it. The inner band is deliberately not a second published
   * limit: it is a "this is drifting" hint, so a reading that the manual would
   * pass but that sits near the edge is still visibly different from one that
   * sits on nominal.
   *
   * A min/max window has no published centre, so "near the edge" is measured
   * from the edges instead: within 10% of the window's width of either limit
   * is marginal. A one-sided limit has only the one edge, and a reading
   * within 5% of the bound (range.tol) on the passing side is marginal.
   * Percent off nominal is not reported for a one-sided limit: there is no
   * nominal to be off from, only a bound not to cross.
   */
  TestPoints.evaluate = function (state, measured) {
    var range = TestPoints.range(state);
    if (range == null || measured == null || isNaN(measured)) return null;
    var deviation = measured - range.nominal;
    var oneSided = range.kind === 'min' || range.kind === 'max';
    // Percent off nominal is meaningless against a nominal of zero, which is
    // exactly the "should read less than 1 V" case, so report volts there.
    var pct = (oneSided || range.nominal === 0) ? null
      : (deviation / Math.abs(range.nominal)) * 100;
    var inRange = measured >= range.lo && measured <= range.hi;
    var margin, verdict;
    if (range.kind === 'minmax') {
      var width = range.hi - range.lo;
      var toEdge = Math.min(measured - range.lo, range.hi - measured);
      // Fraction of the half-window used, same scale as the other kinds:
      // 1 at a limit, 0 at the centre.
      margin = range.tol === 0 ? 1 : Math.abs(deviation) / range.tol;
      verdict = !inRange ? 'fail' : (width > 0 && toEdge <= width * 0.1 ? 'marginal' : 'pass');
    } else if (oneSided) {
      // Distance from the bound on the passing side, as a fraction of the
      // near-limit band: 0 at the bound, 1 at the band's far edge.
      var clear = range.kind === 'min' ? measured - range.lo : range.hi - measured;
      margin = range.tol === 0 ? (clear > 0 ? 0 : 1) : Math.max(0, 1 - clear / range.tol);
      verdict = !inRange ? 'fail' : (clear <= range.tol ? 'marginal' : 'pass');
    } else {
      margin = range.tol === 0 ? 1 : Math.abs(deviation) / range.tol;
      verdict = !inRange ? 'fail' : (margin <= 0.5 ? 'pass' : 'marginal');
    }
    return {
      verdict: verdict,
      measured: measured,
      nominal: range.nominal,
      lo: range.lo,
      hi: range.hi,
      tol: range.tol,
      deviation: deviation,
      pctOffNominal: pct,
      // How much of the allowed tolerance this reading uses up, 0..1+.
      usedTolerance: margin
    };
  };

  TestPoints.formatRange = function (state, unit) {
    var range = TestPoints.range(state);
    if (!range) return '—';
    var u = unit || 'V';
    // A ceiling around zero is a statement about the reading's magnitude, and
    // has to read as one: the limit gets no sign, because it is a bound, not a
    // level. A maxAbs curated against a nonzero nominal is an ordinary band
    // and falls through to the lo … hi form, which is what it actually means.
    if (range.kind === 'maxAbs' && range.nominal === 0) {
      return '|reading| ≤ ' + magnitude(range.tol) + ' ' + u;
    }
    // A one-sided limit is a bound, not a band: "≤ 60 V", "≥ 24 V". No plus
    // sign on the bound -- it reads as a limit, not a level -- but a negative
    // one keeps its minus, because -24 V and +24 V are different places to
    // put a probe.
    if (range.kind === 'max') return '≤ ' + bound(range.hi, range.tol) + ' ' + u;
    if (range.kind === 'min') return '≥ ' + bound(range.lo, range.tol) + ' ' + u;
    var pct = state.tolerancePct != null ? ' (±' + state.tolerancePct + '%)' : '';
    return fmt(range.lo, range.tol) + ' … ' + fmt(range.hi, range.tol) + ' ' + u + pct;
  };

  TestPoints.formatNominal = function (state, unit) {
    var range = TestPoints.range(state);
    if (!range) return '—';
    // A one-sided limit has no nominal to print, so the bound stands in for
    // it -- the same text as the accept range, because that is all the manual
    // says.
    if (range.kind === 'min' || range.kind === 'max') {
      return TestPoints.formatRange(state, unit);
    }
    // The nominal is signed because -565 V and +565 V are different places to
    // put a probe; the tolerance either side of it is not. The nominal also
    // may not print coarser than its own band: 1.2288 MHz ± 0.002 rounded to
    // "+1.23" disagrees with the tolerance beside it.
    return fmt(range.nominal, range.tol) + ' ' + (unit || 'V') + ' ± ' + magnitude(range.tol);
  };

  /**
   * Decimal places for a value — and, when the band around it is narrower than
   * the value's own print precision, for the band. 32 MHz held to ±0.1% is a
   * 0.032 MHz tolerance: printed to the whole-number precision the magnitude
   * alone would pick, both ends round to "+32" and the accept range reads as a
   * point. So the finer of the two magnitudes chooses, and below 1 the count
   * follows the leading significant digit rather than stopping at three,
   * capped so a degenerate tolerance cannot ask for a page of zeros.
   */
  function digitsFor(v, tol) {
    var a = Math.abs(v);
    if (tol != null && isFinite(tol) && tol > 0 && tol < a) a = tol;
    if (a >= 100) return 0;
    if (a >= 10) return 1;
    if (a >= 1) return 2;
    if (a === 0) return 3;
    return Math.max(3, Math.min(6, Math.ceil(-Math.log(a) / Math.LN10) + 1));
  }

  function trim(s) {
    return /\./.test(s) ? s.replace(/0+$/, '').replace(/\.$/, '') : s;
  }

  function fmt(v, tol) {
    if (v == null || isNaN(v)) return '—';
    // The open side of a one-sided limit: there is no number to print.
    if (!isFinite(v)) return '';
    return (v > 0 ? '+' : '') + trim(v.toFixed(digitsFor(v, tol)));
  }

  function bound(v, tol) {
    var s = fmt(v, tol);
    return s.charAt(0) === '+' ? s.slice(1) : s;
  }

  function magnitude(v) {
    if (v == null) return '—';
    return trim(Math.abs(v).toFixed(digitsFor(v)));
  }

  TestPoints.fmt = fmt;
  TestPoints.magnitude = magnitude;

  /** Group the assembly's test points by supply rail, in a stable order. */
  TestPoints.byRail = function (dataset) {
    var rails = dataset.rails || {};
    var order = Object.keys(rails);
    var groups = {};
    (dataset.testpoints || []).forEach(function (tp) {
      var key = tp.rail || 'OTHER';
      (groups[key] = groups[key] || []).push(tp);
    });
    Object.keys(groups).forEach(function (key) {
      groups[key].sort(function (a, b) {
        // Returns last within a rail: the supplies are what you measure, the
        // return is what you clip the black lead to.
        if (!!a.isReturn !== !!b.isReturn) return a.isReturn ? 1 : -1;
        return numOf(a.ref) - numOf(b.ref);
      });
    });
    return order.filter(function (k) { return groups[k]; })
      .map(function (k) {
        return { id: k, label: (rails[k] || {}).label || k,
                 com: (rails[k] || {}).com, color: (rails[k] || {}).color,
                 testpoints: groups[k] };
      })
      .concat(groups.OTHER ? [{ id: 'OTHER', label: 'Other', testpoints: groups.OTHER }] : []);
  };

  function numOf(ref) {
    var m = /(\d+)$/.exec(ref || '');
    return m ? parseInt(m[1], 10) : 0;
  }

  global.TestPoints = TestPoints;
})(window);

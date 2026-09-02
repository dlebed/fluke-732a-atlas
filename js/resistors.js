/*
 * resistors.js — which resistors are worth pulling, and what the parts list
 * says the one in your hand should read.
 *
 * The capacitor audit next door asks one question: how close does the rail run
 * to the part's rating. A resistor on these boards has no equivalent question
 * — nothing here dissipates a quarter of what it is rated for — so this asks
 * the other question a bench asks, which is what the part is made of.
 *
 * Carbon composition is the family that moves. The element is graphite in a
 * phenolic binder; the binder takes up moisture and the part drifts UP,
 * permanently once it has aged, and worst where the value is high — a high
 * value is a leaner graphite mix to begin with. Fluke's tolerance on every one
 * of these is ±5%; a forty-year-old EB-series part sitting +10% or +20% is
 * ordinary rather than remarkable. That is what makes them a rework family:
 * the drift is the age, not a fault.
 *
 * Nothing else on these three boards is in that position, and the lookalikes
 * matter:
 *
 *   RES, CF        carbon FILM — a deposited film on a ceramic rod, a
 *                  different part with a different failure mode and a good
 *                  deal more stable. A3 R19, added by the 7/85 errata.
 *   RES, DEP. CAR  deposited carbon, the same construction under the older
 *                  name. A4 R24, A5 R44/R45 family.
 *   RES, MTL. FILM / WW / CERMET
 *                  stable by construction. A reading out of tolerance on one
 *                  of these is a fault, not age, and belongs in the log rather
 *                  than in a replacement round.
 *
 * All of them are classified and labelled here; only COMP is ever offered for
 * wholesale replacement.
 */
(function (global) {
  'use strict';

  var Res = {};

  /**
   * The family, off the description's second field.
   *
   * The same place Caps.type reads a capacitor's, and the same reason it is
   * anchored on a word boundary rather than the start of the string. The
   * second field is a class name, not a value, so it stops at the next comma
   * or full stop — "RES, MTL. FILM, 1.54K" is metal film, and the stop inside
   * the abbreviation is part of the name.
   */
  function resType(item) {
    var desc = (item && item.desc) || '';
    if (/\bSET\b/i.test(desc) && !/\bRES,\s*(COMP|WW|CF)\b/i.test(desc)) return 'SET';
    var m = /\bRES[,.]\s*([A-Z][A-Z. ]*?)\s*(?:,|$)/i.exec(desc);
    if (!m) return null;
    var t = m[1].toUpperCase().replace(/\s+/g, ' ').replace(/\.$/, '');
    // A pot names its element after the word VAR ("RES, VAR, CERMET, 5K"); a
    // pot that does not is just a pot.
    if (t === 'VAR') {
      var el = /\bRES,\s*VAR,\s*([A-Z][A-Z. ]*?)\s*,/i.exec(desc);
      return el ? 'VAR ' + el[1].toUpperCase().replace(/\.$/, '') : 'VAR';
    }
    return TYPE_ALIASES[t] || t;
  }
  Res.type = resType;

  // One name per construction, whichever way the table abbreviates it.
  var TYPE_ALIASES = {
    'MTL FILM': 'MF', 'MTL. FILM': 'MF', 'METAL FILM': 'MF', 'MF': 'MF',
    'DEP CAR': 'DEPCAR', 'DEP. CAR': 'DEPCAR', 'DEPOSITED CARBON': 'DEPCAR',
    'CARBON COMP': 'COMP', 'COMPOSITION': 'COMP'
  };

  var TYPE_LABELS = {
    COMP: 'Carbon composition', CF: 'Carbon film', DEPCAR: 'Deposited carbon',
    MF: 'Metal film', WW: 'Wirewound', CERMET: 'Cermet', VAR: 'Variable',
    'VAR CERMET': 'Cermet trimmer', SET: 'Matched set'
  };
  Res.typeLabel = function (t) { return TYPE_LABELS[t] || t || 'Resistor'; };

  /** Only carbon composition is a rework family; see the note at the top. */
  Res.isComposition = function (item) { return resType(item) === 'COMP'; };

  /**
   * A resistance as a technician types it: "510", "10k", "4.7K", "1M".
   *
   * Returned as {value, unit} rather than a bare number of ohms, so the log
   * stores 10.4 kΩ where 10.4k was typed instead of 10400 Ω — the reading
   * reads back in the unit it was taken in, beside a parts list that prints
   * the same one. A bare number is ohms. Nothing here means milliohms: "m" is
   * megohms on a resistor row, which is what these boards are lettered in and
   * what anyone typing it means.
   */
  Res.parse = function (text) {
    var raw = String(text == null ? '' : text).trim().replace(',', '.');
    if (!raw) return null;
    var m = /^(\d*\.?\d+)\s*([kKmM])?\s*(?:R|OHMS?|Ω)?$/.exec(raw);
    if (!m) return null;
    var value = parseFloat(m[1]);
    if (isNaN(value)) return null;
    var suffix = (m[2] || '').toUpperCase();
    var unit = suffix === 'K' ? 'kΩ' : (suffix === 'M' ? 'MΩ' : 'Ω');
    return { value: value, unit: unit, base: value * (suffix === 'K' ? 1e3 : suffix === 'M' ? 1e6 : 1) };
  };

  /**
   * Everything the parts list states about one resistor.
   *
   * Deliberately log-free, exactly like the capacitor audit: what a part has
   * measured belongs to a unit and a visit, and mixing it in here would make
   * the audit answer differently for two instruments on the same bench.
   * Returns null for anything that is not a resistor.
   */
  Res.audit = function (item, dataset) {
    if (!item || item.kind !== 'res') return null;
    var d = dataset || (global.BoardExplorer && global.BoardExplorer.state.assembly);
    if (!d) return null;
    var Parts = global.Parts;
    var spec = Parts ? Parts.spec(item) : null;
    if (spec && spec.quantity !== 'resistance') spec = null;
    var limits = spec && Parts ? Parts.limits(spec) : null;
    var type = resType(item);
    var watts = Parts ? Parts.ratedPower(item) : null;

    return {
      kind: 'res',
      ref: item.ref,
      assembly: d.id,
      type: type,
      typeLabel: Res.typeLabel(type),
      isComposition: type === 'COMP',
      // Table 5-6 stars the reference parts: §4-53 says the reference is not
      // field repairable, so these are shown and never bulk-ticked.
      starred: !!item.star,
      spec: spec,
      value: spec ? spec.base : null,
      valueText: spec && Parts ? Parts.format(spec.base, 'resistance', spec.unit) : '',
      tolerancePct: limits ? limits.hi : null,
      toleranceText: spec && Parts ? Parts.toleranceText(spec) : '',
      limits: limits,
      powerW: watts,
      powerText: Parts ? Parts.powerText(watts) : '',
      // What the curated dataset says this position does — the resistor
      // equivalent of the capacitor's traced net, and the only thing on the
      // row that says whether pulling it is a five minute job or a decision.
      note: item.function || null,
      item: item
    };
  };

  /**
   * How far a reading is off what the table prints, and whether that is a
   * failure by the table's own tolerance.
   *
   * The verdict is Parts.compare's, unchanged — a component tolerance is what
   * the part left the factory at, so 'fail' means genuinely outside it. What
   * this adds is the sentence to put on screen, because "+7.2%" on its own
   * does not say against what.
   */
  Res.judge = function (item, ohms) {
    var Parts = global.Parts;
    if (!Parts || ohms == null || isNaN(ohms)) return null;
    var spec = Parts.spec(item);
    if (!spec || spec.quantity !== 'resistance') return null;
    var scored = Parts.compare(spec, ohms);
    if (!scored) return null;
    var limits = Parts.limits(spec);
    var pct = scored.pctOffNominal;
    var text = (pct > 0 ? '+' : '') + pct.toFixed(1) + '%';
    return {
      pctOffNominal: pct,
      verdict: scored.verdict,
      limits: limits,
      // Carbon composition drifts up, so which way it went is worth saying:
      // a part 8% high is doing what these do, one 8% low is something else.
      label: text + ' of ' + Parts.format(spec.base, 'resistance', spec.unit) +
        (limits
          ? (scored.verdict === 'fail'
              ? ' — outside ' + Parts.toleranceText(spec)
              : ' — inside ' + Parts.toleranceText(spec))
          : ' — the table prints no tolerance')
    };
  };

  /**
   * Every resistor on a board, audited.
   *
   * Ordered largest value first, because that is the order carbon composition
   * fails in: the drift is a percentage of a value that is already a lean mix,
   * and the megohm positions move furthest. Ties fall back to the designator
   * so the list is stable between renders.
   */
  Res.list = function (dataset, opts) {
    var d = dataset || (global.BoardExplorer && global.BoardExplorer.state.assembly);
    if (!d) return [];
    var options = opts || {};
    var out = [];
    (d.components || []).forEach(function (c) {
      if (c.kind !== 'res') return;
      var a = Res.audit(c, d);
      if (!a) return;
      if (options.types && options.types.indexOf(a.type) < 0) return;
      out.push(a);
    });
    out.sort(byValue);
    return out;
  };

  Res.listAll = function (opts) {
    var BE = global.BoardExplorer;
    if (!BE) return [];
    var out = [];
    BE.list().forEach(function (d) {
      Res.list(d, opts).forEach(function (a) {
        // A part the interconnect view only mirrors is the board's part, and
        // the board's own row is the one to tick. See BoardExplorer.mirrors.
        if (BE.mirrors(a.item)) return;
        out.push(a);
      });
    });
    out.sort(byValue);
    return out;
  };

  function byValue(x, y) {
    var xv = x.value == null ? -1 : x.value;
    var yv = y.value == null ? -1 : y.value;
    if (xv !== yv) return yv - xv;
    if (x.assembly !== y.assembly) {
      return global.Caps ? global.Caps.sortAsm(x.assembly, y.assembly)
                         : (x.assembly < y.assembly ? -1 : 1);
    }
    return x.ref < y.ref ? -1 : 1;
  }
  Res.sortByValue = byValue;

  /** How many of each family a dataset (or the whole instrument) carries. */
  Res.summary = function (scope) {
    var rows = scope === 'all' ? Res.listAll() : Res.list(scope);
    var counts = {};
    rows.forEach(function (a) { counts[a.type] = (counts[a.type] || 0) + 1; });
    return counts;
  };

  global.Res = Res;
})(window);

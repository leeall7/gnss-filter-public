const b = require('@protomaps/basemaps');
const { validateStyleMin } = require('@maplibre/maplibre-gl-style-spec');
const fs = require('fs');
console.log('uk у мовах:', b.language_script_pairs.some(p => p.lang === 'uk'));

// «День»: теплий приглушений фон, дороги білі з чіткою обводкою, магістралі — янтарні.
const day = { ...b.namedFlavor('light'),
  background: '#efeae1', earth: '#efeae1',
  park_a: '#d6e6c8', park_b: '#cfe1bf', wood_a: '#d3e3c4', wood_b: '#c9dcb8', scrub_a: '#dde8cf', scrub_b: '#d6e3c6',
  water: '#a9cbe6', buildings: '#e0d9cd',
  hospital: '#f2dcdc', school: '#ece3cf', industrial: '#e6e1d8', military: '#e6dcd6', aerodrome: '#e4e1ea',
  highway: '#f6c46a', highway_casing_early: '#c98f2c', highway_casing_late: '#c98f2c',
  major: '#ffffff', major_casing_early: '#b9b1a4', major_casing_late: '#b9b1a4',
  link: '#ffffff', link_casing: '#b9b1a4',
  minor_a: '#ffffff', minor_b: '#ffffff', minor_service: '#f8f5ef', minor_casing: '#cfc7ba', minor_service_casing: '#d8d1c5',
  railway: '#a39c91', boundaries: '#9b8fa8',
};
// «Ніч»: глибокий синьо-сірий, дороги світлі, магістралі — приглушений янтар.
const night = { ...b.namedFlavor('dark'),
  background: '#151a21', earth: '#1b212a',
  water: '#0f2a3d', buildings: '#262d38',
  park_a: '#1d2b24', park_b: '#1f2e26', wood_a: '#1c2a23', wood_b: '#1e2c24',
  highway: '#b98a3e', highway_casing_early: '#6d5122', highway_casing_late: '#6d5122',
  major: '#4a5566', major_casing_early: '#2b323d', major_casing_late: '#2b323d',
  link: '#4a5566', minor_a: '#39424f', minor_b: '#39424f', minor_service: '#323a46',
};
function style(name, flavor) {
  return {
    version: 8,
    name: 'GNSS Nav — ' + name,
    glyphs: '{GLYPHS}/{fontstack}/{range}.pbf',
    sprite: '{SPRITE}',
    sources: { protomaps: { type: 'vector', url: 'pmtiles://{PMTILES}',
      attribution: '© OpenStreetMap contributors · Protomaps' } },
    layers: b.layers('protomaps', flavor, { lang: 'uk' }),
  };
}
for (const [file, name, fl] of [['style-day.json', 'День', day], ['style-night.json', 'Ніч', night]]) {
  const s = style(name, fl);
  // валідатор не знає плейсхолдерів — підставляємо зразкові значення лише для перевірки
  // шрифти — під назвами тек в архіві (без пробілів: шлях до локального файла не залежить від кодування URL)
  let txt = JSON.stringify(s).replace(/Noto Sans Regular/g, 'NotoSans-Regular').replace(/Noto Sans Medium/g, 'NotoSans-Medium')
    .replace(/Noto Sans Italic/g, 'NotoSans-Italic').replace(/Noto Sans Devanagari Regular v1/g, 'NotoSans-Regular');
  const sOut = JSON.parse(txt);
  const probe = JSON.parse(txt.replace('{GLYPHS}', 'file:///fonts').replace('{SPRITE}', 'file:///sprites/light')
    .replace('pmtiles://{PMTILES}', 'pmtiles://file:///map.pmtiles'));
  const errs = validateStyleMin(probe);
  const fonts = new Set();
  for (const l of sOut.layers) { const f = l.layout && l.layout['text-font']; if (f) f.forEach(x => fonts.add(x)); }
  const icons = s.layers.filter(l => l.layout && l.layout['icon-image']).length;
  console.log(file, 'шарів', s.layers.length, 'помилок', errs.length, errs.slice(0,3).map(e => e.message), 'шрифти', [...fonts], 'шарів зі значками', icons);
  fs.writeFileSync(file, JSON.stringify(sOut));
}

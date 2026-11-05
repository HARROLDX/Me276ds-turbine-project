/* Curved particle veil for the project hero. Attach to <canvas id="particles">. */
(() => {
  'use strict';

  function mount() {
    const canvas = document.querySelector('canvas#particles');
    if (!canvas || canvas.dataset.particleVeilMounted) return;
    const ctx = canvas.getContext('2d', { alpha: false });
    if (!ctx) return;
    canvas.dataset.particleVeilMounted = '1';

    const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
    const colors = [[134, 185, 245], [179, 211, 255], [218, 232, 255], [148, 140, 227]];
    const TAU = Math.PI * 2;
    const smooth = x => (x = Math.max(0, Math.min(1, x)), x * x * (3 - 2 * x));

    // Sprites keep the handful of out-of-focus particles soft without per-frame filters.
    const glow = colors.map(([r, g, b]) => {
      const sprite = document.createElement('canvas');
      sprite.width = sprite.height = 64;
      const c = sprite.getContext('2d');
      const grad = c.createRadialGradient(32, 32, 0, 32, 32, 32);
      for (const [stop, opacity] of [[0, .85], [.28, .69], [.53, .27], [.76, .07], [1, 0]]) {
        grad.addColorStop(stop, 'rgba(' + [r, g, b, opacity].join(',') + ')');
      }
      c.fillStyle = grad;
      c.fillRect(0, 0, 64, 64);
      return sprite;
    });

    let width, height, dpr, backdrop;
    let dots = [], bokeh = [], frameId = 0, elapsed = 0, lastFrame = 0, onScreen = true;

    function prepare() {
      const box = canvas.getBoundingClientRect();
      width = Math.max(1, Math.round(box.width));
      height = Math.max(1, Math.round(box.height));
      dpr = Math.min(devicePixelRatio || 1, width < 640 ? 1.5 : 2);
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      let state = 843219;
      const random = () => {
        state = (Math.imul(1664525, state) + 1013904223) >>> 0;
        return state / 4294967296;
      };
      // Composite the stationary haze once. The left side stays dark behind page copy.
      backdrop = document.createElement('canvas');
      backdrop.width = width;
      backdrop.height = height;
      const bg = backdrop.getContext('2d');
      bg.fillStyle = '#04060a';
      bg.fillRect(0, 0, width, height);
      for (const [x, y, size, color] of [[.96, .28, .41, '22,36,66'], [.78, .89, .34, '20,24,46']]) {
        const g = bg.createRadialGradient(x * width, y * height, 0, x * width, y * height, size * width);
        g.addColorStop(0, 'rgba(' + color + ',.65)');
        g.addColorStop(1, 'rgba(' + color + ',0)');
        bg.fillStyle = g;
        bg.fillRect(0, 0, width, height);
      }

      dots = [];
      bokeh = [];
      const count = Math.round(Math.min(16900, Math.max(2900, width * height / 69)));
      const radiusScale = Math.max(.70, Math.min(1.35, Math.sqrt(width / 1410)));
      const mobile = width < 650;
      for (let i = 0; i < count; i++) {
        const u = random() * 1.54 - .25;
        const v = random() * 2 - 1;
        const fold = u * 7 - .75;
        const twist = 2.8 * v + fold;
        const silhouette = Math.cos(twist);
        const depth = Math.sin(twist);
        const crest = Math.pow(Math.abs(silhouette), 5);
        const widthFactor = .87 + .24 * Math.sin(u * 4 + .7);
        const spine = .952 - .365 * smooth((u - .36) / .70) + .022 * Math.sin(6 * u + .3);
        // A turning, rippling sheet. Its projected folds concentrate points into bright ridges.
        let x = spine + widthFactor * (.100 * silhouette + .064 * v + .026 * Math.sin(10 * u + 4.2 * v));
        let y = u + .088 * depth + .055 * v * Math.sin(6.1 * u - .75)
          + .018 * Math.sin(11 * u + 5 * v);
        const diffuse = random() < .24;
        if (diffuse) {
          x += (random() - .48) * .14;
          y += (random() - .5) * .115;
        }
        if (mobile) x = .39 + x * .73;
        const focus = .25 + .75 * smooth((depth + 1.2) / 1.8);
        const alpha = (.14 + .64 * random()) * (.44 + .56 * crest)
          * (diffuse ? .57 : 1) * (.65 + .35 * focus);
        const purple = smooth((x - .73) * 4) * (.56 + .44 * Math.sin(u * 6 - .82));
        const color = random() < purple * .63 ? 3 : random() < .29 + .31 * crest ? 2 : random() < .53 ? 1 : 0;
        const phase = 5.3 * u + 2.8 * v;
        dots.push({
          x, y, sx: Math.sin(phase), cx: Math.cos(phase),
          sy: Math.sin(phase * .92 + .95), cy: Math.cos(phase * .92 + .95),
          radius: (.39 + .78 * random() ** 2 + .52 * crest) * radiusScale,
          style: 'rgba(' + [...colors[color], Math.min(.95, alpha).toFixed(3)].join(',') + ')'
        });
        if (diffuse && random() < .075) {
          bokeh.push({ x: x + (random() - .5) * .14, y: y + (random() - .5) * .11,
            size: (3 + 19 * random() ** 2) * radiusScale, alpha: .07 + .24 * random(),
            phase: random() * TAU, color });
        }
      }
      // Rows on the focal sheet form a finer woven texture. Projection compresses the
      // rows at each turn, creating the silvery contours without drawing a solid band.
      const lanes = mobile ? 43 : 76;
      const steps = mobile ? 89 : 152;
      for (let lane = 0; lane < lanes; lane++) {
        for (let j = 0; j < steps; j++) {
          const u = (j + random() * .80) / steps * 1.34 - .14;
          const v = (lane + random() * .36) / lanes * 2 - 1;
          const a = 8.7 * u - 1.55;
          const ripple = Math.sin(6 * u + 1.9 * v);
          const spine = .940 - .35 * smooth((u - .34) / .73)
            + .032 * Math.sin(6.2 * u + .1);
          let x = spine + .029 * Math.sin(10 * u + .7)
            + .078 * v * Math.cos(a) + .027 * ripple + .022 * v * v;
          const y = u + .086 * v * Math.sin(a) + .033 * Math.sin(9 * u + 2.4 * v);
          if (mobile) x = .39 + x * .73;
          const rim = Math.abs(v);
          const shine = .36 + .64 * Math.abs(Math.sin(a + v * .95));
          const shade = random();
          const color = (x > .8 && shade < .23) ? 3 : shade < .70 ? 2 : 1;
          const alpha = Math.min(.92, (.31 + .40 * random() + .22 * rim ** 3) * shine);
          const phase = 5.3 * u + .5 * v;
          dots.push({ x, y, sx: Math.sin(phase), cx: Math.cos(phase),
            sy: Math.sin(phase * .92 + .95), cy: Math.cos(phase * .92 + .95),
            radius: (.66 + 1.08 * random() ** 1.5 + .25 * rim) * radiusScale,
            style: 'rgba(' + [...colors[color], alpha.toFixed(3)].join(',') + ')' });
        }
      }
      draw();
    }

    function draw() {
      if (!backdrop) return;
      const clock = elapsed * .00014;
      const s = Math.sin(clock), c = Math.cos(clock);
      const sy = Math.sin(clock * .84), cy = Math.cos(clock * .84);
      ctx.globalAlpha = 1;
      ctx.drawImage(backdrop, 0, 0);
      for (const p of bokeh) {
        ctx.globalAlpha = p.alpha;
        const px = width * (p.x + .009 * Math.sin(p.phase + clock));
        const py = height * (p.y + .013 * Math.cos(p.phase - clock));
        ctx.drawImage(glow[p.color], px - p.size, py - p.size, p.size * 2, p.size * 2);
      }
      ctx.globalAlpha = 1;
      for (const p of dots) {
        const px = width * (p.x + .013 * (p.sx * c + p.cx * s));
        const py = height * (p.y + .014 * (p.sy * cy + p.cy * sy));
        ctx.fillStyle = p.style;
        ctx.fillRect(px, py, p.radius, p.radius);
      }
    }

    function animate(now) {
      frameId = 0;
      if (document.hidden || !onScreen || reduceMotion.matches) return;
      // At 24 fps the slowly moving surface looks continuous and leaves room for scrolling.
      if (!lastFrame || now - lastFrame >= 1000 / 24) {
        elapsed += lastFrame ? Math.min(now - lastFrame, 90) : 0;
        lastFrame = now;
        draw();
      }
      frameId = requestAnimationFrame(animate);
    }
    function sync() {
      cancelAnimationFrame(frameId);
      frameId = lastFrame = 0;
      if (!document.hidden && onScreen && !reduceMotion.matches) frameId = requestAnimationFrame(animate);
    }

    prepare();
    let lastWidth = width, lastHeight = height;
    const resize = () => {
      const { width: w, height: h } = canvas.getBoundingClientRect();
      if (Math.round(w) === lastWidth && Math.round(h) === lastHeight) return;
      prepare();
      lastWidth = width;
      lastHeight = height;
    };
    if (window.ResizeObserver) new ResizeObserver(resize).observe(canvas);
    else window.addEventListener('resize', resize);
    if (window.IntersectionObserver) new IntersectionObserver(entries => {
      onScreen = entries[0].isIntersecting;
      sync();
    }).observe(canvas);
    document.addEventListener('visibilitychange', sync);
    if (reduceMotion.addEventListener) reduceMotion.addEventListener('change', sync);
    else reduceMotion.addListener(sync);
    sync();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
  else mount();
})();

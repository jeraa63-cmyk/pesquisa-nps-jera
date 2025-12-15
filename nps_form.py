def escala_0a10(key: str) -> int:
    if f"{key}__touched" not in st.session_state:
        st.session_state[f"{key}__touched"] = False
    if key not in st.session_state:
        st.session_state[key] = 0

    if not st.session_state.get(f"{key}__touched", False):
        st.markdown("<p class='slider-instruction'>Deslize para responder</p>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='height: 1.0rem;'></div>", unsafe_allow_html=True)

    # ✅ Slider real (invisível via CSS pelo aria-label)
    val = st.slider(
        label="__nps_hidden__",
        min_value=0,
        max_value=10,
        value=st.session_state[key],
        step=1,
        key=key,
        on_change=_touch,
        args=(key,),
        label_visibility="collapsed",
    )

    pct = (val / 10) * 100.0

    ticks_html = []
    for n in range(0, 11):
        left = (n / 10) * 100.0
        cls = "nps-tick selected" if n == val else "nps-tick"
        ticks_html.append(
            f"<span class='{cls}' style='left:{left:.6f}%' data-n='{n}'>{n}</span>"
        )
    ticks_html = "\n".join(ticks_html)

    st.components.v1.html(
        f"""
        <style>
          :root {{
            --jera-primary:#00C1AD;
            --jera-dark:#052B38;
          }}

          .nps-wrap {{
            width: 100%;
            max-width: 860px;
            margin: 0.6rem auto 0.2rem auto;
            position: relative;
            font-family: Arial, sans-serif;
          }}

          .nps-bar {{
            height: 4px;
            background: rgba(0,193,173,0.35);
            border-radius: 999px;
            position: relative;
            margin: 0.7rem 0 0.9rem 0;
          }}

          .nps-bar-fill {{
            height: 4px;
            background: var(--jera-primary);
            border-radius: 999px;
            width: {pct:.6f}%;
          }}

          .nps-knob {{
            width: 18px;
            height: 18px;
            background: var(--jera-primary);
            border-radius: 999px;
            position: absolute;
            top: 50%;
            left: {pct:.6f}%;
            transform: translate(-50%,-50%);
            box-shadow: 0 6px 14px rgba(0,0,0,.18);
          }}

          .nps-axis {{
            position: relative;
            height: 28px;
          }}

          .nps-tick {{
            position: absolute;
            top: 0;
            transform: translateX(-50%);
            font-size: 14px;
            color: var(--jera-dark);
            cursor: pointer;
            user-select: none;
            line-height: 1;
            padding: 2px 7px;
            border-radius: 10px;
            white-space: nowrap;
          }}

          .nps-tick.selected {{
            color: #fff !important;
            background: var(--jera-primary);
            font-weight: 700;
          }}

          .nps-tick:hover {{
            background: rgba(0,193,173,0.15);
          }}
        </style>

        <div class="nps-wrap" id="nps-wrap">
          <div class="nps-bar">
            <div class="nps-bar-fill"></div>
            <div class="nps-knob"></div>
          </div>
          <div class="nps-axis">
            {ticks_html}
          </div>
        </div>

        <script>
          (function() {{
            function findNpsSliderInput() {{
              const doc = window.parent.document;

              // procura o slider pelo aria-label do BaseWeb
              const base = doc.querySelector('[data-baseweb="slider"][aria-label="__nps_hidden__"]');
              if (!base) return null;

              const inp = base.querySelector('input[type="range"]');
              return inp || null;
            }}

            const slider = findNpsSliderInput();
            const root = document.getElementById("nps-wrap");
            if (!root || !slider) return;

            const ticks = root.querySelectorAll(".nps-tick");

            function setValue(n) {{
              slider.value = n;
              slider.dispatchEvent(new Event('input', {{ bubbles: true }}));
              slider.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}

            ticks.forEach(t => {{
              t.addEventListener("click", () => {{
                const n = parseInt(t.getAttribute("data-n"), 10);
                setValue(n);
              }});
            }});
          }})();
        </script>
        """,
        height=110,
    )

    return val

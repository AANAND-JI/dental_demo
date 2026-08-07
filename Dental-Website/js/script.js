/* =========================================================
   ToothWise Dental Clinic — script.js  (shared, all pages)
   Vanilla JavaScript — no dependencies.
   ---------------------------------------------------------
   Every feature is guarded so the single shared file runs
   safely on any page, executing only what exists in the DOM.
   ---------------------------------------------------------
   FEATURES
   1.  Sticky navbar shrink on scroll
   2.  Mobile hamburger menu + mobile dropdown
   3.  Desktop dropdown keyboard support
   4.  Counter animations
   5.  Scroll reveal (IntersectionObserver)
   6.  Skill / progress bar animation
   7.  Back-to-top button
   8.  FAQ accordion + FAQ search
   9.  Testimonials slider (auto + manual)
   10. Gallery lightbox
   11. Category filters (gallery, testimonials)
   12. Contact / appointment / newsletter validation
   13. Lazy loading fallback
   14. Dynamic footer year
   ========================================================= */

(function () {
    "use strict";

    const $  = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

    document.addEventListener("DOMContentLoaded", init);

    function init() {
        stickyHeader();
        mobileMenu();
        dropdowns();
        counters();
        scrollReveal();
        skillBars();
        backToTop();
        faqAccordion();
        faqSearch();
        testimonialSlider();
        lightbox();
        filters();
        formValidation();
        appointmentForm();
        newsletterForm();
        lazyLoadFallback();
        setFooterYear();
    }

    /* =====================================================
       1. STICKY HEADER
       ===================================================== */
    function stickyHeader() {
        const header = $("#site-header");
        if (!header) return;
        const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 30);
        onScroll();
        window.addEventListener("scroll", onScroll, { passive: true });
    }

    /* =====================================================
       2. MOBILE HAMBURGER MENU
       ===================================================== */
    function mobileMenu() {
        const burger = $("#hamburger");
        const menu = $("#nav-menu");
        if (!burger || !menu) return;

        const toggle = (open) => {
            const willOpen = typeof open === "boolean" ? open : !menu.classList.contains("open");
            menu.classList.toggle("open", willOpen);
            burger.classList.toggle("active", willOpen);
            burger.setAttribute("aria-expanded", String(willOpen));
            document.body.style.overflow = willOpen ? "hidden" : "";
        };

        burger.addEventListener("click", () => toggle());

        /* Close when a real (non-dropdown-toggle) link is clicked */
        $$(".nav-menu a", menu).forEach((link) =>
            link.addEventListener("click", () => {
                if (!link.classList.contains("dropdown-toggle")) toggle(false);
            })
        );

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && menu.classList.contains("open")) toggle(false);
        });

        document.addEventListener("click", (e) => {
            if (
                menu.classList.contains("open") &&
                !menu.contains(e.target) &&
                !burger.contains(e.target)
            ) {
                toggle(false);
            }
        });
    }

    /* =====================================================
       3. DROPDOWN (mobile toggle + accessibility)
       ===================================================== */
    function dropdowns() {
        $$(".has-dropdown").forEach((dd) => {
            const toggle = $(".dropdown-toggle", dd);
            if (!toggle) return;

            toggle.addEventListener("click", (e) => {
                /* On mobile the caret expands the submenu instead of navigating */
                if (window.innerWidth <= 900) {
                    e.preventDefault();
                    dd.classList.toggle("open");
                }
            });
        });
    }

    /* =====================================================
       4. ANIMATED COUNTERS
       ===================================================== */
    function counters() {
        const nums = $$("[data-count]");
        if (!nums.length) return;

        const animate = (el) => {
            const target = parseInt(el.dataset.count, 10) || 0;
            const suffix = el.dataset.suffix || "";
            const duration = 1800;
            const start = performance.now();
            const step = (now) => {
                const p = Math.min((now - start) / duration, 1);
                const eased = 1 - Math.pow(1 - p, 3);
                el.textContent = Math.floor(eased * target).toLocaleString() + suffix;
                if (p < 1) requestAnimationFrame(step);
                else el.textContent = target.toLocaleString() + suffix;
            };
            requestAnimationFrame(step);
        };

        const obs = new IntersectionObserver(
            (entries, o) => entries.forEach((en) => {
                if (en.isIntersecting) { animate(en.target); o.unobserve(en.target); }
            }),
            { threshold: 0.4 }
        );
        nums.forEach((n) => obs.observe(n));
    }

    /* =====================================================
       5. SCROLL REVEAL
       ===================================================== */
    function scrollReveal() {
        const items = $$(".reveal");
        if (!items.length) return;
        if (!("IntersectionObserver" in window)) {
            items.forEach((i) => i.classList.add("visible"));
            return;
        }
        const obs = new IntersectionObserver(
            (entries, o) => entries.forEach((en, i) => {
                if (en.isIntersecting) {
                    setTimeout(() => en.target.classList.add("visible"), i * 70);
                    o.unobserve(en.target);
                }
            }),
            { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
        );
        items.forEach((i) => obs.observe(i));
    }

    /* =====================================================
       6. SKILL / PROGRESS BARS
       ===================================================== */
    function skillBars() {
        const bars = $$(".skill__fill");
        if (!bars.length) return;
        const obs = new IntersectionObserver(
            (entries, o) => entries.forEach((en) => {
                if (en.isIntersecting) {
                    const el = en.target;
                    el.style.width = (el.dataset.level || "0") + "%";
                    o.unobserve(el);
                }
            }),
            { threshold: 0.4 }
        );
        bars.forEach((b) => obs.observe(b));
    }

    /* =====================================================
       7. BACK TO TOP
       ===================================================== */
    function backToTop() {
        const btn = $("#back-to-top");
        if (!btn) return;
        window.addEventListener(
            "scroll",
            () => btn.classList.toggle("show", window.scrollY > 500),
            { passive: true }
        );
        btn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
    }

    /* =====================================================
       8. FAQ ACCORDION
       ===================================================== */
    function faqAccordion() {
        const items = $$(".faq-item");
        if (!items.length) return;
        items.forEach((item) => {
            const btn = $(".faq-item__q", item);
            const panel = $(".faq-item__a", item);
            btn.addEventListener("click", () => {
                const isOpen = item.classList.contains("open");
                items.forEach((o) => {
                    o.classList.remove("open");
                    $(".faq-item__q", o).setAttribute("aria-expanded", "false");
                    $(".faq-item__a", o).style.maxHeight = null;
                });
                if (!isOpen) {
                    item.classList.add("open");
                    btn.setAttribute("aria-expanded", "true");
                    panel.style.maxHeight = panel.scrollHeight + "px";
                }
            });
        });
        window.addEventListener("resize", () => {
            const open = $(".faq-item.open .faq-item__a");
            if (open) open.style.maxHeight = open.scrollHeight + "px";
        });
    }

    /* =====================================================
       8b. FAQ SEARCH
       ===================================================== */
    function faqSearch() {
        const input = $("#faq-search");
        if (!input) return;
        const items = $$(".faq-item");
        const empty = $("#faq-empty");

        input.addEventListener("input", () => {
            const q = input.value.trim().toLowerCase();
            let shown = 0;
            items.forEach((item) => {
                const text = item.textContent.toLowerCase();
                const match = text.includes(q);
                item.classList.toggle("is-hidden", !match);
                if (match) shown++;
            });
            if (empty) empty.hidden = shown !== 0;
        });
    }

    /* =====================================================
       9. TESTIMONIALS SLIDER
       ===================================================== */
    function testimonialSlider() {
        const track = $("#slider-track");
        if (!track) return;
        const slides = $$(".slide", track);
        const dotsWrap = $("#slider-dots");
        const prevBtn = $("#slide-prev");
        const nextBtn = $("#slide-next");
        const slider = $("#testimonial-slider");
        if (slides.length === 0) return;

        let index = 0, timer = null;
        const INTERVAL = 6000;

        slides.forEach((_, i) => {
            const dot = document.createElement("button");
            dot.setAttribute("role", "tab");
            dot.setAttribute("aria-label", `Go to testimonial ${i + 1}`);
            if (i === 0) dot.classList.add("active");
            dot.addEventListener("click", () => goTo(i));
            dotsWrap.appendChild(dot);
        });
        const dots = $$("button", dotsWrap);

        function update() {
            track.style.transform = `translateX(-${index * 100}%)`;
            dots.forEach((d, i) => d.classList.toggle("active", i === index));
        }
        function goTo(i) { index = (i + slides.length) % slides.length; update(); restart(); }
        const next = () => goTo(index + 1);
        const prev = () => goTo(index - 1);
        const start = () => (timer = setInterval(next, INTERVAL));
        const stop = () => clearInterval(timer);
        const restart = () => { stop(); start(); };

        nextBtn && nextBtn.addEventListener("click", next);
        prevBtn && prevBtn.addEventListener("click", prev);
        slider.addEventListener("mouseenter", stop);
        slider.addEventListener("mouseleave", start);
        slider.addEventListener("focusin", stop);
        slider.addEventListener("focusout", start);
        slider.addEventListener("keydown", (e) => {
            if (e.key === "ArrowRight") next();
            if (e.key === "ArrowLeft") prev();
        });

        let startX = 0;
        track.addEventListener("touchstart", (e) => (startX = e.touches[0].clientX), { passive: true });
        track.addEventListener("touchend", (e) => {
            const diff = e.changedTouches[0].clientX - startX;
            if (Math.abs(diff) > 50) diff < 0 ? next() : prev();
        }, { passive: true });

        update();
        start();
    }

    /* =====================================================
       10. GALLERY LIGHTBOX
       ===================================================== */
    function lightbox() {
        const items = $$(".gallery__item");
        const box = $("#lightbox");
        if (!items.length || !box) return;
        const img = $("#lightbox-img");
        const closeBtn = $("#lightbox-close");
        const prevBtn = $("#lightbox-prev");
        const nextBtn = $("#lightbox-next");

        /* Only lightbox currently-visible items */
        const visible = () => items.filter((el) => !el.classList.contains("is-hidden"));
        let list = [], current = 0;

        function open(el) {
            list = visible();
            current = list.indexOf(el);
            show();
            box.classList.add("open");
            box.setAttribute("aria-hidden", "false");
            document.body.style.overflow = "hidden";
            closeBtn.focus();
        }
        function close() {
            box.classList.remove("open");
            box.setAttribute("aria-hidden", "true");
            document.body.style.overflow = "";
        }
        function show() {
            const el = list[current];
            img.src = el.dataset.full;
            img.alt = $("img", el) ? $("img", el).alt : "";
        }
        const next = () => { current = (current + 1) % list.length; show(); };
        const prev = () => { current = (current - 1 + list.length) % list.length; show(); };

        items.forEach((el) => el.addEventListener("click", () => open(el)));
        closeBtn.addEventListener("click", close);
        nextBtn.addEventListener("click", next);
        prevBtn.addEventListener("click", prev);
        box.addEventListener("click", (e) => { if (e.target === box) close(); });
        document.addEventListener("keydown", (e) => {
            if (!box.classList.contains("open")) return;
            if (e.key === "Escape") close();
            if (e.key === "ArrowRight") next();
            if (e.key === "ArrowLeft") prev();
        });
    }

    /* =====================================================
       11. CATEGORY FILTERS (gallery, testimonials)
       ===================================================== */
    function filters() {
        $$("[data-filter-group]").forEach((group) => {
            const buttons = $$(".filter-btn", group);
            const targetSel = group.dataset.filterTarget;
            const items = $$(targetSel);

            buttons.forEach((btn) => {
                btn.addEventListener("click", () => {
                    buttons.forEach((b) => b.classList.remove("active"));
                    btn.classList.add("active");
                    const cat = btn.dataset.filter;
                    items.forEach((item) => {
                        const show = cat === "all" || item.dataset.category === cat;
                        item.classList.toggle("is-hidden", !show);
                    });
                });
            });
        });
    }

    /* =====================================================
       12a. CONTACT FORM VALIDATION
       ===================================================== */
    function formValidation() {
        const form = $("#contact-form");
        if (!form) return;
        validateForm(form, {
            name:    { test: (v) => v.trim().length >= 2, msg: "Please enter your full name." },
            email:   { test: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()), msg: "Please enter a valid email address." },
            phone:   { test: (v) => /^[+\d][\d\s()-]{6,}$/.test(v.trim()), msg: "Please enter a valid phone number." },
            message: { test: (v) => v.trim().length >= 10, msg: "Please enter a message (min 10 characters)." },
        }, "#form-success");
    }

    /* =====================================================
       12b. APPOINTMENT FORM VALIDATION
       ===================================================== */
    function appointmentForm() {
        const form = $("#appointment-form");
        if (!form) return;
        validateForm(form, {
            name:  { test: (v) => v.trim().length >= 2, msg: "Please enter your full name." },
            email: { test: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()), msg: "Please enter a valid email address." },
            phone: { test: (v) => /^[+\d][\d\s()-]{6,}$/.test(v.trim()), msg: "Please enter a valid phone number." },
            date:  { test: (v) => v.trim() !== "", msg: "Please choose a preferred date." },
            time:  { test: (v) => v.trim() !== "", msg: "Please choose a preferred time." },
        }, "#appointment-success");
    }

    /* Shared validation engine */
    function validateForm(form, rules, successSel) {
        const success = $(successSel);

        function validateField(field) {
            const rule = rules[field.name];
            if (!rule) return true;
            const group = field.closest(".form-group");
            const error = $(`.form-error[data-for="${field.name}"]`, form);
            const ok = rule.test(field.value);
            if (group) group.classList.toggle("invalid", !ok);
            if (error) error.textContent = ok ? "" : rule.msg;
            return ok;
        }

        Object.keys(rules).forEach((name) => {
            const field = form.elements[name];
            if (!field) return;
            field.addEventListener("blur", () => validateField(field));
            field.addEventListener("input", () => {
                const g = field.closest(".form-group");
                if (g && g.classList.contains("invalid")) validateField(field);
            });
        });

        form.addEventListener("submit", (e) => {
            e.preventDefault();
            let valid = true, firstInvalid = null;
            Object.keys(rules).forEach((name) => {
                const field = form.elements[name];
                if (!field) return;
                const ok = validateField(field);
                if (!ok && !firstInvalid) firstInvalid = field;
                if (!ok) valid = false;
            });
            if (!valid) { firstInvalid && firstInvalid.focus(); return; }
            if (success) success.hidden = false;
            form.reset();
            if (success) setTimeout(() => (success.hidden = true), 6000);
        });
    }

    /* =====================================================
       12c. NEWSLETTER FORM
       ===================================================== */
    function newsletterForm() {
        const form = $("#newsletter-form");
        if (!form) return;
        const msg = $("#newsletter-msg");
        const input = $("#newsletter-email");
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const ok = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
            if (!ok) { input.focus(); input.style.borderColor = "#e5484d"; return; }
            input.style.borderColor = "";
            if (msg) msg.hidden = false;
            form.reset();
            if (msg) setTimeout(() => (msg.hidden = true), 6000);
        });
    }

    /* =====================================================
       13. LAZY LOADING FALLBACK
       ===================================================== */
    function lazyLoadFallback() {
        if ("loading" in HTMLImageElement.prototype) return;
        const lazy = $$('img[loading="lazy"]');
        if (!lazy.length || !("IntersectionObserver" in window)) return;
        const obs = new IntersectionObserver((entries, o) => {
            entries.forEach((en) => {
                if (en.isIntersecting) {
                    const img = en.target;
                    if (img.dataset.src) img.src = img.dataset.src;
                    o.unobserve(img);
                }
            });
        });
        lazy.forEach((img) => obs.observe(img));
    }

    /* =====================================================
       14. DYNAMIC FOOTER YEAR
       ===================================================== */
    function setFooterYear() {
        $$("#year, .year").forEach((el) => (el.textContent = new Date().getFullYear()));
    }
})();

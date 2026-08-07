#!/usr/bin/env python3
# =========================================================
# ToothWise — static multi-page site generator (build tool)
# Produces static HTML files with all text written inline.
# No runtime JS/JSON content loading is used by the site.
# =========================================================
import os, html

OUT = "/home/user/Dental-Website"

# ----------------------------------------------------------------------
# Reusable inline SVG icons
# ----------------------------------------------------------------------
IC = {
    "tick": '<svg viewBox="0 0 24 24"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>',
    "star": '<svg viewBox="0 0 24 24"><path d="m12 2 3 6.5 7 .6-5.3 4.6L18.2 21 12 17.3 5.8 21l1.5-7.3L2 9.1l7-.6z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.5 15.5 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.58 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .57 3.6 1 1 0 0 1-.25 1z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 10.4-3.7 2.1-1-1.7L11 11V6h2z"/></svg>',
    "fb": '<svg viewBox="0 0 24 24"><path d="M13 22v-8h3l.5-3H13V9.2c0-.9.3-1.5 1.6-1.5H16.6V5.1A22 22 0 0 0 14.3 5c-2.3 0-3.8 1.4-3.8 3.9V11H8v3h2.5v8z"/></svg>',
    "tw": '<svg viewBox="0 0 24 24"><path d="M22 5.9c-.7.3-1.5.5-2.3.6a4 4 0 0 0 1.8-2.2c-.8.5-1.7.8-2.6 1a4 4 0 0 0-6.8 3.6A11.3 11.3 0 0 1 3.9 4.8a4 4 0 0 0 1.2 5.3c-.6 0-1.2-.2-1.8-.5a4 4 0 0 0 3.2 3.9c-.5.2-1.1.2-1.7.1a4 4 0 0 0 3.7 2.8A8 8 0 0 1 2 18.1 11.3 11.3 0 0 0 20.5 8.5c.8-.6 1.5-1.4 2-2.3z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.3 2.2.4.6.2 1 .5 1.4 1 .4.4.7.8 1 1.4.2.5.4 1.1.4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.3 1.8-.4 2.2-.2.6-.5 1-1 1.4-.4.4-.8.7-1.4 1-.5.2-1.1.4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.3-2.2-.4-.6-.2-1-.5-1.4-1-.4-.4-.7-.8-1-1.4-.2-.5-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.3-1.8.4-2.2.2-.6.5-1 1-1.4.4-.4.8-.7 1.4-1 .5-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 3.2A6.6 6.6 0 1 0 18.6 12 6.6 6.6 0 0 0 12 5.4zm0 10.9A4.3 4.3 0 1 1 16.3 12 4.3 4.3 0 0 1 12 16.3zm6.9-11.1a1.5 1.5 0 1 1-1.5-1.5 1.5 1.5 0 0 1 1.5 1.5z"/></svg>',
    "in": '<svg viewBox="0 0 24 24"><path d="M6.9 8H4V20h2.9zM5.4 3.5A1.7 1.7 0 1 0 5.4 7a1.7 1.7 0 0 0 0-3.5zM20 20h-2.9v-5.9c0-1.4 0-3.2-2-3.2s-2.3 1.5-2.3 3.1V20H10V8h2.8v1.6h.1c.4-.7 1.4-1.6 3-1.6 3.1 0 3.7 2 3.7 4.7z"/></svg>',
    "send": '<svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg>',
    "search": '<svg viewBox="0 0 24 24"><path d="M10 2a8 8 0 1 0 4.9 14.3l5.4 5.4 1.4-1.4-5.4-5.4A8 8 0 0 0 10 2zm0 2a6 6 0 1 1 0 12 6 6 0 0 1 0-12z"/></svg>',
    "up": '<svg viewBox="0 0 24 24"><path d="M12 5l-7 7 1.4 1.4L11 8.8V20h2V8.8l4.6 4.6L19 12z"/></svg>',
    "left": '<svg viewBox="0 0 24 24"><path d="M15 6 9 12l6 6"/></svg>',
    "right": '<svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>',
    "cap": '<svg viewBox="0 0 24 24"><path d="M12 3 1 9l11 6 9-4.9V17h2V9zM5 13.2V17c0 1.7 3.1 3 7 3s7-1.3 7-3v-3.8l-7 3.8z"/></svg>',
    "award": '<svg viewBox="0 0 24 24"><path d="M12 2a6 6 0 0 0-3 11.2V22l3-2 3 2v-8.8A6 6 0 0 0 12 2zm0 2a4 4 0 1 1 0 8 4 4 0 0 1 0-8z"/></svg>',
    "heart": '<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-10-9.3C.4 8.4 2 5 5.3 5c2 0 3.2 1 3.7 2 .5-1 1.7-2 3.7-2 3.3 0 4.9 3.4 3.3 6.7C19.5 16.4 12 21 12 21z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24"><path d="M12 2 3 6v6c0 5 3.8 9.4 9 10 5.2-.6 9-5 9-10V6zm-1 13-4-4 1.4-1.4L11 12.2l4.6-4.6L17 9z"/></svg>',
    "smile": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM8 9a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0zm5 0a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0zm-5.3 5h8.6a4.5 4.5 0 0 1-8.6 0z"/></svg>',
    "tooth": '<svg viewBox="0 0 24 24"><path d="M12 2C8 2 6.5 4 4.5 4S2 3 2 6c0 4 1 9 2.5 12 1 2 1.6 3 2.5 3 1.3 0 1-3 2.5-3s1.2 3 2.5 3c.9 0 1.5-1 2.5-3C17.5 15 18 10 18 6c0-3-1-2-2.5-2S15 2 12 2z"/></svg>',
    "target": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 4a6 6 0 1 1 0 12 6 6 0 0 1 0-12zm0 3a3 3 0 1 0 0 6 3 3 0 0 0 0-6z"/></svg>',
    "eye": '<svg viewBox="0 0 24 24"><path d="M12 5c-5 0-9.3 3.1-11 7 1.7 3.9 6 7 11 7s9.3-3.1 11-7c-1.7-3.9-6-7-11-7zm0 11a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm0-6a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/></svg>',
    "users": '<svg viewBox="0 0 24 24"><path d="M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10zm0 2c-4 0-8 2-8 6v2h16v-2c0-4-4-6-8-6z"/></svg>',
    "cog": '<svg viewBox="0 0 24 24"><path d="M19.4 13a7.8 7.8 0 0 0 0-2l2-1.6-2-3.4-2.4 1a7.5 7.5 0 0 0-1.7-1l-.4-2.6h-4l-.4 2.6a7.5 7.5 0 0 0-1.7 1l-2.4-1-2 3.4L4 11a7.8 7.8 0 0 0 0 2l-2 1.6 2 3.4 2.4-1a7.5 7.5 0 0 0 1.7 1l.4 2.6h4l.4-2.6a7.5 7.5 0 0 0 1.7-1l2.4 1 2-3.4zM12 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"/></svg>',
    "plus": '<svg viewBox="0 0 24 24"><path d="M11 2h2v6h6v2h-6v6h-2v-6H5V8h6z"/></svg>',
    "money": '<svg viewBox="0 0 24 24"><path d="M12 1 3 5v6c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V5zm1 15h-2v-2h2zm0-4h-2V7h2z"/></svg>',
    "chip": '<svg viewBox="0 0 24 24"><path d="M9 3v2H7v14h10V5h-2V3H9zm0 6h6v2H9V9zm0 4h6v2H9v-2z"/></svg>',
    "cal": '<svg viewBox="0 0 24 24"><path d="M7 2v2H5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-2V2h-2v2H9V2zM5 9h14v10H5z"/></svg>',
}

SERVICE_ICONS = {
    "General Dentistry": IC["tooth"],
    "Root Canal Therapy": '<svg viewBox="0 0 24 24"><path d="M12 2a4 4 0 0 0-4 4c0 1.5.5 2 .5 4S8 17 9 20c.5 1.5 1 2 1.5 2s.8-1 1-3 .5-3 1-3 .8 1 1 3 .5 3 1 3 1-.5 1.5-2c1-3 .5-8 .5-10s.5-2.5.5-4a4 4 0 0 0-4-4z"/></svg>',
    "Dental Implants": '<svg viewBox="0 0 24 24"><path d="M12 2C8 2 6.5 4 4.5 4S2 3 2 6c0 4 1 9 2.5 12 1 2 1.6 3 2.5 3 1.3 0 1-3 2.5-3s1.2 3 2.5 3c.9 0 1.5-1 2.5-3C17.5 15 18 10 18 6c0-3-1-2-2.5-2S15 2 12 2z"/></svg>',
    "Cosmetic Dentistry": IC["shield"],
    "Orthodontics": '<svg viewBox="0 0 24 24"><path d="M4 10h16v2H4zm2 4h12v2H6zm2-8h8v2H8z"/></svg>',
    "Teeth Whitening": '<svg viewBox="0 0 24 24"><path d="M12 2C8 2 6.5 4 4.5 4S2 3 2 6c0 4 1 9 2.5 12 1 2 1.6 3 2.5 3 1.3 0 1-3 2.5-3s1.2 3 2.5 3c.9 0 1.5-1 2.5-3C17.5 15 18 10 18 6c0-3-1-2-2.5-2S15 2 12 2z"/><circle cx="19" cy="5" r="2.5"/></svg>',
    "Pediatric Dentistry": '<svg viewBox="0 0 24 24"><path d="M12 2a4 4 0 0 0-4 4c0 3-1 4-1 8 0 4 1 6 2 6s1-2 1.5-3.5S12 18 12 18s.5 1 1 2.5S14 22 15 22s2-2 2-6c0-4-1-5-1-8a4 4 0 0 0-4-4z"/><circle cx="12" cy="7" r="1.3" fill="#fff"/></svg>',
    "Emergency Dental Care": IC["plus"],
    "Dental Bridges & Crowns": IC["cog"],
}

# Services data (title, short desc)
SERVICES = [
    ("General Dentistry", "Routine exams, professional cleanings, fillings and preventive care that keep your smile healthy year-round."),
    ("Root Canal Therapy", "Advanced, virtually painless endodontic treatment that saves damaged teeth and ends deep tooth pain fast."),
    ("Dental Implants", "Permanent, natural-looking tooth replacement that restores full bite strength, comfort and confidence."),
    ("Cosmetic Dentistry", "Veneers, bonding and full smile makeovers crafted to give you a brighter, perfectly balanced smile."),
    ("Orthodontics", "Traditional braces and clear aligners that gently straighten teeth and correct bite for all ages."),
    ("Teeth Whitening", "Safe, professional whitening that removes years of stains for a dazzling, camera-ready smile in one visit."),
    ("Pediatric Dentistry", "Gentle, fun and fear-free dental care that helps children build healthy habits and happy smiles."),
    ("Emergency Dental Care", "Same-day relief for broken teeth, severe pain and accidents — available around the clock, every day."),
]

DOCTORS = [
    ("doctor1.jpg", "Dr. Ruth Miller", "Oral Surgery & Extractions", "BDS, MDS — Oral & Maxillofacial Surgery"),
    ("doctor2.jpg", "Dr. Alex Turner", "Endodontics & Root Canal", "BDS, MDS — Conservative Dentistry"),
    ("doctor3.jpg", "Dr. Ami Wilburn", "Implantology", "BDS, MDS — Prosthodontics & Implants"),
    ("doctor4.jpg", "Dr. Basilio Ettore", "General & Cosmetic Dentist", "BDS — Aesthetic & Restorative Dentistry"),
]

BLOGS = [
    ("blog1.jpg", "Cosmetic", "July 24, 2026", "2026-07-24", "Dr. Basilio Ettore",
     "5 Simple Habits For A Brighter, Whiter Smile",
     "Discover the everyday routines — from the foods you eat to the way you brush — that keep your smile radiant between professional whitening visits."),
    ("blog2.jpg", "Prevention", "June 30, 2026", "2026-06-30", "Dr. Alex Turner",
     "Why Regular Check-Ups Save You Money",
     "Preventive dentistry catches small problems before they become painful — and expensive. Here's how a six-month visit protects both your teeth and your wallet."),
    ("blog3.jpg", "Implants", "June 12, 2026", "2026-06-12", "Dr. Ami Wilburn",
     "Dental Implants: What To Expect Step By Step",
     "Considering implants? We break down the entire journey — from consultation to your final, confident smile — so you know exactly what to expect."),
]

# ----------------------------------------------------------------------
# Shared layout pieces
# ----------------------------------------------------------------------
def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#1E90FF" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <meta name="author" content="ToothWise Dental Clinic" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="assets/images/hero.jpg" />
    <link rel="icon" href="favicon.ico" sizes="any" />
    <link rel="icon" type="image/png" href="assets/images/favicon.png" />
    <link rel="stylesheet" href="css/style.css" />
    <link rel="stylesheet" href="css/responsive.css" />
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
'''

NAV = [
    ("home", "Home", "index.html"),
    ("about", "About", "about.html"),
    ("services", "Services", "services.html"),
    ("doctors", "Doctors", "doctors.html"),
    ("blog", "Blog", "blog.html"),
    ("contact", "Contact", "contact.html"),
]
DROPDOWN = [
    ("gallery", "Gallery", "gallery.html"),
    ("testimonials", "Testimonials", "testimonials.html"),
    ("pricing", "Pricing", "pricing.html"),
    ("faq", "FAQ", "faq.html"),
]
# which top-level owns which detail page
OWNER = {"service-details": "services", "doctor-details": "doctors", "blog-single": "blog"}
DROPDOWN_KEYS = {k for k, _, _ in DROPDOWN}

def header(active):
    owner = OWNER.get(active, active)
    # Build main links (insert dropdown before Blog)
    items = ""
    for key, label, href in NAV:
        if key == "blog":
            # inject Pages dropdown right before Blog
            dd_parent_active = " active" if owner in DROPDOWN_KEYS else ""
            dd_items = ""
            for dk, dl, dh in DROPDOWN:
                a = " active" if owner == dk else ""
                dd_items += f'<a href="{dh}" class="{a.strip()}">{dl}</a>'
            items += f'''<li class="has-dropdown{ (' open' if False else '') }">
                    <a href="pricing.html" class="nav-link dropdown-toggle{dd_parent_active}" aria-haspopup="true">Pages
                        <svg class="dropdown-caret" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 10l5 5 5-5z"/></svg>
                    </a>
                    <div class="dropdown">{dd_items}</div>
                </li>'''
        a = " active" if owner == key else ""
        items += f'<li><a href="{href}" class="nav-link{a}">{label}</a></li>'

    return f'''    <header class="site-header" id="site-header">
        <div class="topbar">
            <div class="container topbar__inner">
                <ul class="topbar__contacts">
                    <li><span class="ic">{IC["pin"]}</span><span>221B Baker Street, London, England</span></li>
                    <li><span class="ic">{IC["mail"]}</span><a href="mailto:hello@toothwise.com">hello@toothwise.com</a></li>
                </ul>
                <ul class="topbar__contacts">
                    <li><span class="ic">{IC["phone"]}</span><a href="tel:+447908712026">+44 7908 712 026</a></li>
                    <li><span class="ic">{IC["clock"]}</span><span>Mon–Sat, 9:00am – 5:00pm</span></li>
                </ul>
            </div>
        </div>
        <nav class="navbar" aria-label="Primary navigation">
            <div class="container navbar__inner">
                <a href="index.html" class="brand" aria-label="ToothWise home">
                    <svg class="brand__logo" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2c-2 0-2.5 1-4.5 1S4 2 3 3.5C1.6 5.6 2.4 9 3.2 12.5c.6 2.6 1 6.5 2.6 6.5 1.4 0 1.3-3 2.7-3s1.4 3 3 3 1.6-3.9 2.2-6.5C16.6 9 17.4 5.6 16 3.5 15 2 13.5 3 12 3S12 2 12 2z" transform="translate(2,0)"/></svg>
                    <span class="brand__name">Tooth<span>Wise</span></span>
                </a>
                <ul class="nav-menu" id="nav-menu">
                    {items}
                </ul>
                <a href="appointment.html" class="btn btn--primary nav-cta">Book Appointment</a>
                <button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="nav-menu">
                    <span></span><span></span><span></span>
                </button>
            </div>
        </nav>
    </header>
'''

def banner(title, crumb):
    # crumb: list of (label, href) with last item href=None (current)
    parts = []
    for i, (label, href) in enumerate(crumb):
        if href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
        if i < len(crumb) - 1:
            parts.append('<span class="sep">/</span>')
    crumbs = "".join(parts)
    return f'''    <section class="page-banner">
        <img src="assets/images/hero.jpg" alt="" class="page-banner__bg" aria-hidden="true" />
        <div class="container page-banner__inner">
            <h1>{title}</h1>
            <nav class="breadcrumb" aria-label="Breadcrumb">{crumbs}</nav>
        </div>
    </section>
'''

def footer():
    return f'''    <footer class="footer" id="footer">
        <div class="container footer__grid">
            <div class="footer__col">
                <a href="index.html" class="brand brand--light">
                    <svg class="brand__logo" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2c-2 0-2.5 1-4.5 1S4 2 3 3.5C1.6 5.6 2.4 9 3.2 12.5c.6 2.6 1 6.5 2.6 6.5 1.4 0 1.3-3 2.7-3s1.4 3 3 3 1.6-3.9 2.2-6.5C16.6 9 17.4 5.6 16 3.5 15 2 13.5 3 12 3S12 2 12 2z" transform="translate(2,0)"/></svg>
                    <span class="brand__name">Tooth<span>Wise</span></span>
                </a>
                <p class="footer__about">Modern, painless and genuinely personal dental care. We're here to help you smile with confidence — for life.</p>
                <div class="footer__social">
                    <a href="https://facebook.com" aria-label="ToothWise on Facebook">{IC["fb"]}</a>
                    <a href="https://twitter.com" aria-label="ToothWise on Twitter">{IC["tw"]}</a>
                    <a href="https://instagram.com" aria-label="ToothWise on Instagram">{IC["ig"]}</a>
                    <a href="https://linkedin.com" aria-label="ToothWise on LinkedIn">{IC["in"]}</a>
                </div>
            </div>
            <div class="footer__col">
                <h3 class="footer__title">Quick Links</h3>
                <ul class="footer__links">
                    <li><a href="about.html">About Us</a></li>
                    <li><a href="doctors.html">Our Doctors</a></li>
                    <li><a href="gallery.html">Gallery</a></li>
                    <li><a href="pricing.html">Pricing</a></li>
                    <li><a href="blog.html">Blog</a></li>
                    <li><a href="contact.html">Contact</a></li>
                </ul>
            </div>
            <div class="footer__col">
                <h3 class="footer__title">Services</h3>
                <ul class="footer__links">
                    <li><a href="service-details.html">General Dentistry</a></li>
                    <li><a href="service-details.html">Dental Implants</a></li>
                    <li><a href="service-details.html">Cosmetic Dentistry</a></li>
                    <li><a href="service-details.html">Orthodontics</a></li>
                    <li><a href="service-details.html">Teeth Whitening</a></li>
                    <li><a href="service-details.html">Emergency Care</a></li>
                </ul>
            </div>
            <div class="footer__col">
                <h3 class="footer__title">Working Hours</h3>
                <ul class="footer__hours">
                    <li><span>Mon – Fri</span><span>9:00am – 5:00pm</span></li>
                    <li><span>Saturday</span><span>9:00am – 2:00pm</span></li>
                    <li><span>Sunday</span><span>Emergency Only</span></li>
                </ul>
                <h3 class="footer__title footer__title--news">Newsletter</h3>
                <form class="newsletter" id="newsletter-form" novalidate>
                    <label for="newsletter-email" class="sr-only">Email address</label>
                    <input type="email" id="newsletter-email" name="newsletter-email" placeholder="Your email address" required />
                    <button type="submit" class="btn btn--primary" aria-label="Subscribe to newsletter">{IC["send"]}</button>
                </form>
                <p class="newsletter__msg" id="newsletter-msg" role="status" hidden>You're subscribed — welcome to ToothWise!</p>
            </div>
        </div>
        <div class="footer__bottom">
            <div class="container footer__bottom-inner">
                <p>&copy; <span id="year"></span> ToothWise Dental Clinic. All rights reserved.</p>
                <ul class="footer__legal">
                    <li><a href="privacy-policy.html">Privacy Policy</a></li>
                    <li><a href="terms.html">Terms of Service</a></li>
                </ul>
            </div>
        </div>
    </footer>
    <button class="back-to-top" id="back-to-top" aria-label="Back to top">{IC["up"]}</button>
'''

LIGHTBOX = f'''    <div class="lightbox" id="lightbox" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Image viewer">
        <button class="lightbox__close" id="lightbox-close" aria-label="Close image viewer">&times;</button>
        <button class="lightbox__nav lightbox__nav--prev" id="lightbox-prev" aria-label="Previous image">{IC["left"]}</button>
        <img src="" alt="" class="lightbox__img" id="lightbox-img" />
        <button class="lightbox__nav lightbox__nav--next" id="lightbox-next" aria-label="Next image">{IC["right"]}</button>
    </div>
'''

def scripts():
    return '''    <script src="js/script.js"></script>
</body>
</html>
'''

def page(fname, title, desc, active, body, lightbox=False):
    doc = head(title, desc) + header(active) + '    <main id="main">\n' + body + '    </main>\n' + footer()
    if lightbox:
        doc += LIGHTBOX
    doc += scripts()
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(doc)
    print("wrote", fname, len(doc), "bytes")

# ----------------------------------------------------------------------
# Component builders
# ----------------------------------------------------------------------
def stars(n=5):
    return '<div class="stars" aria-label="Rated %d out of 5 stars">%s</div>' % (n, IC["star"]*n)

def service_card(title, desc):
    return f'''<article class="service-card reveal">
        <span class="service-card__icon" aria-hidden="true">{SERVICE_ICONS.get(title, IC["tooth"])}</span>
        <h3>{title}</h3>
        <p>{desc}</p>
        <a href="service-details.html" class="link-more">Read More <span aria-hidden="true">&rarr;</span></a>
    </article>'''

def doctor_card(img, name, spec, qual):
    return f'''<article class="doctor-card reveal">
        <div class="doctor-card__media">
            <a href="doctor-details.html"><img src="assets/images/{img}" alt="Portrait of {name}" loading="lazy" /></a>
            <div class="doctor-card__social">
                <a href="https://facebook.com" aria-label="{name} on Facebook">{IC["fb"]}</a>
                <a href="https://twitter.com" aria-label="{name} on Twitter">{IC["tw"]}</a>
                <a href="https://linkedin.com" aria-label="{name} on LinkedIn">{IC["in"]}</a>
            </div>
        </div>
        <div class="doctor-card__body">
            <h3><a href="doctor-details.html">{name}</a></h3>
            <span class="doctor-card__spec">{spec}</span>
            <p class="doctor-card__qual">{qual}</p>
        </div>
    </article>'''

def blog_card(img, cat, date, dt, author, title, excerpt):
    return f'''<article class="blog-card reveal">
        <a href="blog-single.html" class="blog-card__media">
            <img src="assets/images/{img}" alt="{title}" loading="lazy" />
            <span class="blog-card__cat">{cat}</span>
        </a>
        <div class="blog-card__body">
            <div class="blog-card__meta">
                <time datetime="{dt}">{date}</time><span>By {author}</span>
            </div>
            <h3><a href="blog-single.html">{title}</a></h3>
            <p>{excerpt}</p>
            <a href="blog-single.html" class="link-more">Read More <span aria-hidden="true">&rarr;</span></a>
        </div>
    </article>'''

def why_card(icon, title, desc):
    return f'''<article class="why-card reveal">
        <span class="why-card__icon" aria-hidden="true">{icon}</span>
        <div><h3>{title}</h3><p>{desc}</p></div>
    </article>'''

def mvv_card(icon, title, desc):
    return f'''<article class="mvv-card reveal">
        <span class="mvv-card__icon" aria-hidden="true">{icon}</span>
        <h3>{title}</h3><p>{desc}</p>
    </article>'''

FAQS = [
    ("General", "How often should I visit the dentist?",
     "For most patients we recommend a check-up and professional cleaning every six months. If you have gum disease, implants or ongoing treatment, we may suggest more frequent visits tailored to your needs."),
    ("Treatments", "Does a root canal hurt?",
     "Modern root canal therapy is virtually painless. With effective local anaesthesia and gentle techniques, most patients say it feels no different from having a routine filling — and it relieves the pain they arrived with."),
    ("Treatments", "Are dental implants right for me?",
     "Implants are an excellent, long-lasting solution for most people with one or more missing teeth. During a free consultation we assess your bone health and overall situation to confirm the best option for you."),
    ("Billing", "Do you offer payment plans?",
     "Yes. We believe great dental care should be accessible, so we offer transparent pricing and flexible, interest-free payment plans on many treatments. Our team will walk you through every cost upfront."),
    ("General", "What should I do in a dental emergency?",
     "Call our 24/7 emergency line immediately. For a knocked-out tooth, keep it moist and see us within the hour if possible. We reserve same-day slots for urgent cases such as severe pain, swelling or trauma."),
    ("Treatments", "Is teeth whitening safe?",
     "Professional whitening performed by our dentists is completely safe for your enamel. We use clinically proven products and protect your gums throughout, delivering brighter results than any over-the-counter kit."),
    ("General", "At what age should my child first see a dentist?",
     "We recommend a first visit by your child's first birthday, or when their first tooth appears. Early, positive visits help children build lifelong healthy habits and feel completely at ease in the dental chair."),
    ("Billing", "Do you accept dental insurance?",
     "We work with most major insurance providers and are happy to handle claims paperwork on your behalf. Contact our reception team with your policy details and we'll confirm your coverage before treatment."),
]

def faq_item(cat, q, a, filterable=False):
    attr = f' data-category="{cat}"' if filterable else ""
    return f'''<div class="faq-item"{attr}>
        <button class="faq-item__q" aria-expanded="false"><span>{q}</span><span class="faq-item__icon" aria-hidden="true"></span></button>
        <div class="faq-item__a"><p>{a}</p></div>
    </div>'''

def cta_band(title, text, primary=("Book Appointment","appointment.html"), secondary=("Contact Us","contact.html")):
    sec = f'<a href="{secondary[1]}" class="btn btn--ghost btn--lg">{secondary[0]}</a>' if secondary else ""
    return f'''    <section class="cta-band">
        <div class="container cta-band__inner reveal">
            <h2>{title}</h2>
            <p>{text}</p>
            <div class="hero__actions" style="justify-content:center">
                <a href="{primary[1]}" class="btn btn--light btn--lg">{primary[0]}</a>
                {sec}
            </div>
        </div>
    </section>'''

def section_head(badge, title, sub):
    return f'''<div class="section-head reveal">
        <span class="badge">{badge}</span>
        <h2 class="section-title">{title}</h2>
        <p class="section-subtitle">{sub}</p>
    </div>'''

print("templates loaded")

# ======================================================================
# PAGE: index.html (HOME)
# ======================================================================
hero = f'''    <section class="hero" id="hero">
        <div class="hero__overlay"></div>
        <img src="assets/images/hero.jpg" alt="Friendly ToothWise dental team reviewing patient care in a modern clinic" class="hero__bg" />
        <div class="container hero__inner">
            <div class="hero__content reveal">
                <span class="badge">ToothWise Dental Care</span>
                <h1 class="hero__title">The Art Of <br /><span>Perfecting Smiles</span></h1>
                <p class="hero__text">Gentle, precise and truly personal dental care. From routine check-ups to complete smile makeovers, our certified specialists help you smile with confidence — in comfort, and with no surprises.</p>
                <div class="hero__actions">
                    <a href="appointment.html" class="btn btn--primary btn--lg">Book Appointment</a>
                    <a href="services.html" class="btn btn--ghost btn--lg">Our Services</a>
                </div>
            </div>
        </div>
        <a href="#about-preview" class="scroll-indicator" aria-label="Scroll down">
            <span class="mouse"><span class="wheel"></span></span>
            <span class="scroll-indicator__text">Scroll</span>
        </a>
    </section>'''

about_preview = f'''    <section class="about section" id="about-preview">
        <div class="container about__grid">
            <div class="about__media reveal">
                <img src="assets/images/about1.jpg" alt="Two ToothWise dentists standing together" class="about__img about__img--tall" loading="lazy" />
                <div class="about__col">
                    <img src="assets/images/about2.jpg" alt="Dentist examining a patient's teeth" class="about__img" loading="lazy" />
                    <img src="assets/images/about3.jpg" alt="Dentist explaining a treatment plan" class="about__img" loading="lazy" />
                </div>
                <div class="about__experience">
                    <span class="about__experience-num" data-count="18">0</span>
                    <span class="about__experience-label">Years of Trusted Care</span>
                </div>
            </div>
            <div class="about__content reveal">
                <span class="badge">About Our Clinic</span>
                <h2 class="section-title">Your Great Smile Begins With ToothWise</h2>
                <p class="about__lead">For nearly two decades, ToothWise has been the trusted dental home for thousands of families, blending advanced technology with a warm, patient-first approach.</p>
                <p>From your first consultation to your final polish, our team listens carefully, explains every option, and tailors treatment to your unique needs — so every visit feels calm and completely comfortable.</p>
                <ul class="feature-list">
                    <li><span class="feature-list__icon">{IC["tick"]}</span><div><h3>18+ Years Experience</h3><p>Decades of hands-on dental expertise.</p></div></li>
                    <li><span class="feature-list__icon">{IC["tick"]}</span><div><h3>Modern Equipment</h3><p>Digital, painless, precise dentistry.</p></div></li>
                    <li><span class="feature-list__icon">{IC["tick"]}</span><div><h3>Certified Dentists</h3><p>Fully qualified specialist team.</p></div></li>
                    <li><span class="feature-list__icon">{IC["tick"]}</span><div><h3>24/7 Emergency Care</h3><p>Reassuring help whenever you need it.</p></div></li>
                </ul>
                <a href="about.html" class="btn btn--primary">More About Us</a>
            </div>
        </div>
    </section>'''

featured_services = f'''    <section class="services section section--gray">
        <div class="container">
            {section_head("We Provide", "Best Dental Services For You", "Comprehensive, evidence-based dentistry under one roof — designed to keep your whole family healthy and smiling for life.")}
            <div class="services__grid">
                {"".join(service_card(t, d) for t, d in SERVICES[:8])}
            </div>
            <div class="services__cta reveal"><a href="services.html" class="btn btn--dark btn--lg">View All Services</a></div>
        </div>
    </section>'''

why = f'''    <section class="why section">
        <div class="container">
            {section_head("Why Choose Us", "A Higher Standard Of Dental Care", "We built ToothWise to remove every reason people avoid the dentist — with expertise, honesty and genuine comfort.")}
            <div class="why__grid">
                {why_card(IC["shield"], "Experienced Doctors", "Board-certified specialists with decades of combined clinical excellence.")}
                {why_card(IC["money"], "Affordable Pricing", "Transparent, upfront quotes and flexible payment plans with zero hidden fees.")}
                {why_card(IC["chip"], "Latest Technology", "Digital scanning, 3D imaging and laser dentistry for faster, precise results.")}
                {why_card(IC["plus"], "Emergency Care", "24/7 availability so urgent dental problems never have to wait.")}
                {why_card(IC["users"], "Friendly Staff", "A warm, welcoming team dedicated to making every visit stress-free.")}
                {why_card(IC["cog"], "Sterilized Equipment", "Hospital-grade sterilization protocols to protect your health at every step.")}
            </div>
        </div>
    </section>'''

stats = f'''    <section class="stats" aria-label="Clinic achievements">
        <div class="stats__overlay"></div>
        <div class="container stats__grid">
            <div class="stat reveal"><span class="stat__num" data-count="18" data-suffix="+">0</span><span class="stat__label">Years Experience</span></div>
            <div class="stat reveal"><span class="stat__num" data-count="24000" data-suffix="+">0</span><span class="stat__label">Happy Patients</span></div>
            <div class="stat reveal"><span class="stat__num" data-count="12">0</span><span class="stat__label">Expert Doctors</span></div>
            <div class="stat reveal"><span class="stat__num" data-count="36" data-suffix="+">0</span><span class="stat__label">Awards Won</span></div>
        </div>
    </section>'''

featured_doctors = f'''    <section class="doctors section section--gray">
        <div class="container">
            {section_head("Expert Dental Team", "Meet Our Doctors", "Skilled, compassionate and endlessly dedicated — our specialists make great dentistry feel effortless.")}
            <div class="doctors__grid">
                {"".join(doctor_card(*d) for d in DOCTORS)}
            </div>
            <div class="services__cta reveal"><a href="doctors.html" class="btn btn--dark btn--lg">View All Doctors</a></div>
        </div>
    </section>'''

def testimonial_slide(img, alt, text, name, role):
    return f'''<div class="slide"><blockquote class="testimonial">{stars()}
        <p>{text}</p>
        <footer class="testimonial__author"><img src="assets/images/{img}" alt="Photo of {name}" loading="lazy" /><div><cite>{name}</cite><span>{role}</span></div></footer>
    </blockquote></div>'''

TESTI = [
    ("gallery4.jpg", "Sarah Jennings", "I was terrified of dentists my whole life until I found ToothWise. The team was so patient and gentle that I actually looked forward to my follow-up. My implants look and feel completely natural.", "Sarah Jennings", "Implant Patient"),
    ("doctor3.jpg", "Emily Roberts", "My kids used to dread check-ups. Now they beg to go! The pediatric team makes every visit feel like an adventure, and the clinic is spotless and modern. Highly recommended for families.", "Emily Roberts", "Parent of Two"),
    ("doctor2.jpg", "Daniel Cooper", "The teeth whitening results blew me away — years of coffee stains gone in a single appointment. Professional, transparent pricing and a genuinely lovely team from reception to chair.", "Daniel Cooper", "Cosmetic Patient"),
]

testimonials_preview = f'''    <section class="testimonials section">
        <div class="container">
            {section_head("Happy Patients", "What Our Patients Say", "Real stories from the people who trust us with their smiles every single day.")}
            <div class="slider reveal" id="testimonial-slider">
                <div class="slider__viewport"><div class="slider__track" id="slider-track">
                    {"".join(testimonial_slide(t[0], t[0], t[2], t[3], t[4]) for t in TESTI)}
                </div></div>
                <div class="slider__controls">
                    <button class="slider__btn" id="slide-prev" aria-label="Previous testimonial">{IC["left"]}</button>
                    <div class="slider__dots" id="slider-dots" role="tablist" aria-label="Select testimonial"></div>
                    <button class="slider__btn" id="slide-next" aria-label="Next testimonial">{IC["right"]}</button>
                </div>
            </div>
            <div class="services__cta reveal"><a href="testimonials.html" class="btn btn--dark btn--lg">Read More Reviews</a></div>
        </div>
    </section>'''

latest_blogs = f'''    <section class="blog section section--gray">
        <div class="container">
            {section_head("Latest News", "Our Insights &amp; Articles", "Practical tips, expert advice and the latest in dental health from the ToothWise team.")}
            <div class="blog__grid">{"".join(blog_card(*b) for b in BLOGS)}</div>
            <div class="services__cta reveal"><a href="blog.html" class="btn btn--dark btn--lg">Visit Our Blog</a></div>
        </div>
    </section>'''

home_cta = cta_band("Ready To Transform Your Smile?", "Book your appointment today and take the first step toward healthier, more confident smiles for you and your family.")

page("index.html",
     "ToothWise Dental Clinic | Modern, Painless & Affordable Dental Care",
     "ToothWise is a premium dental clinic offering general dentistry, implants, cosmetic dentistry, orthodontics and 24/7 emergency care. Book your appointment today.",
     "home",
     hero + about_preview + featured_services + why + stats + featured_doctors + testimonials_preview + latest_blogs + home_cta)

# ======================================================================
# PAGE: about.html
# ======================================================================
about_body = banner("About Us", [("Home","index.html"),("About",None)]) + f'''    <section class="section">
        <div class="container split">
            <div class="split__media reveal"><img src="assets/images/about1.jpg" alt="The ToothWise dental team" loading="lazy" /></div>
            <div class="reveal">
                <span class="badge">Our Story</span>
                <h2 class="section-title">Two Decades Of Smiles, Built On Trust</h2>
                <p class="about__lead">ToothWise opened its doors in 2008 with a single dental chair and a big idea: that visiting the dentist could actually be a calm, positive experience.</p>
                <p>What began as a small neighbourhood practice has grown into one of London's most respected dental clinics, welcoming more than twenty-four thousand patients over the years. Through every stage of growth, our founding promise has never changed — honest advice, gentle treatment and genuine care for every person who sits in our chair.</p>
                <p>Today our multidisciplinary team brings together specialists in surgery, implantology, orthodontics and cosmetic dentistry, all working under one roof so your entire family can be cared for in one familiar, friendly place.</p>
                <a href="appointment.html" class="btn btn--primary">Book A Visit</a>
            </div>
        </div>
    </section>
    <section class="section section--gray">
        <div class="container">
            {section_head("What Drives Us", "Mission, Vision &amp; Values", "The principles that shape every decision we make and every smile we care for.")}
            <div class="mvv__grid">
                {mvv_card(IC["target"], "Our Mission", "To deliver exceptional, pain-free dentistry that puts patients first — making world-class oral care accessible, comfortable and stress-free for everyone.")}
                {mvv_card(IC["eye"], "Our Vision", "To be the most trusted dental clinic in the region, setting the standard for compassionate care, clinical excellence and lifelong healthy smiles.")}
                {mvv_card(IC["heart"], "Our Values", "Honesty, empathy, precision and continuous improvement guide us every day — because your trust is the foundation of everything we do.")}
            </div>
        </div>
    </section>
    <section class="section">
        <div class="container">
            {section_head("Our Journey", "A History Of Growth", "From a single chair to a full-service clinic — the milestones that shaped ToothWise.")}
            <div class="timeline">
                <div class="timeline__item reveal"><span class="timeline__year">2008</span><h3>The Beginning</h3><p>ToothWise opens on Baker Street with a single dentist and a promise of gentle, honest care.</p></div>
                <div class="timeline__item reveal"><span class="timeline__year">2013</span><h3>Growing Team</h3><p>We welcome our first specialist surgeons and expand to a five-chair practice.</p></div>
                <div class="timeline__item reveal"><span class="timeline__year">2017</span><h3>Going Digital</h3><p>Investment in 3D imaging, intraoral scanners and laser dentistry transforms patient comfort.</p></div>
                <div class="timeline__item reveal"><span class="timeline__year">2021</span><h3>24/7 Emergency Care</h3><p>We launch round-the-clock emergency dentistry for the whole community.</p></div>
                <div class="timeline__item reveal"><span class="timeline__year">2026</span><h3>24,000+ Smiles</h3><p>Today we proudly care for thousands of families with a team of twelve dedicated specialists.</p></div>
            </div>
        </div>
    </section>
    {stats}
    {cta_band("Experience The ToothWise Difference", "Join the thousands of patients who have made us their dental home. We can't wait to welcome you.")}'''
page("about.html", "About Us | ToothWise Dental Clinic",
     "Learn the ToothWise story — our mission, vision, values, clinic history and the milestones that made us a trusted London dental clinic.",
     "about", about_body)

# ======================================================================
# PAGE: services.html
# ======================================================================
services_body = banner("Our Services", [("Home","index.html"),("Services",None)]) + f'''    <section class="section">
        <div class="container">
            {section_head("We Provide", "Complete Dental Care For Every Need", "Explore our full range of treatments. Click any service to learn more about the procedure, benefits and pricing.")}
            <div class="services__grid">{"".join(service_card(t, d) for t, d in SERVICES)}</div>
        </div>
    </section>
    {why}
    {cta_band("Not Sure Which Treatment You Need?", "Book a friendly consultation and our specialists will recommend the right care for your smile.")}'''
page("services.html", "Services | ToothWise Dental Clinic",
     "From general dentistry and implants to orthodontics, whitening and emergency care — explore ToothWise's complete range of dental services.",
     "services", services_body)

# ======================================================================
# PAGE: service-details.html  (General Dentistry example)
# ======================================================================
related = "".join(service_card(t, d) for t, d in SERVICES[1:4])
sd_faqs = "".join(faq_item(c, q, a) for c, q, a in FAQS[:4])
service_details_body = banner("General Dentistry", [("Home","index.html"),("Services","services.html"),("General Dentistry",None)]) + f'''    <section class="section">
        <div class="container layout">
            <div class="article reveal">
                <img src="assets/images/about2.jpg" alt="Dentist providing general dental care" class="article__img" loading="lazy" />
                <h2 class="mt-0">Comprehensive General Dentistry</h2>
                <p>General dentistry is the foundation of a healthy, confident smile. At ToothWise, our routine and preventive care is designed to catch small issues before they become painful, costly problems — keeping your teeth and gums in excellent shape for life.</p>
                <p>From thorough examinations and professional cleanings to tooth-coloured fillings and gum health treatments, every appointment is unhurried, gentle and tailored to you. We take the time to explain what we see and involve you in every decision about your care.</p>
                <h3>Key Benefits</h3>
                <ul class="ticks">
                    <li>{IC["tick"]}<span>Early detection of cavities, gum disease and oral health concerns.</span></li>
                    <li>{IC["tick"]}<span>Professional cleanings that remove plaque and tartar brushing can't reach.</span></li>
                    <li>{IC["tick"]}<span>Natural-looking, mercury-free tooth-coloured fillings.</span></li>
                    <li>{IC["tick"]}<span>Personalised advice to keep your smile healthy between visits.</span></li>
                </ul>
                <h3>Our Procedure</h3>
                <ol class="steps">
                    <li><strong>Consultation &amp; Exam.</strong> We review your history and carry out a gentle, thorough examination with digital imaging.</li>
                    <li><strong>Diagnosis &amp; Plan.</strong> We explain our findings clearly and build a treatment plan around your goals and budget.</li>
                    <li><strong>Treatment.</strong> Cleaning, fillings or other care is carried out comfortably, at your pace.</li>
                    <li><strong>Prevention &amp; Follow-up.</strong> We schedule your next check-up and share tailored home-care tips.</li>
                </ol>
                <blockquote>"Prevention is always kinder — and cheaper — than cure. A six-month visit is the single best investment you can make in your smile." — Dr. Alex Turner</blockquote>
                <h3>Frequently Asked Questions</h3>
                <div class="faq__list" style="max-width:none">{sd_faqs}</div>
            </div>
            <aside class="sidebar reveal">
                <div class="widget">
                    <h3 class="widget__title">All Services</h3>
                    <ul class="cat-list">
                        {"".join(f'<li><a href="service-details.html">{t}<span aria-hidden="true">&rarr;</span></a></li>' for t,_ in SERVICES)}
                    </ul>
                </div>
                <div class="widget">
                    <h3 class="widget__title">Starting From</h3>
                    <p class="price-card__price" style="margin-bottom:6px">£49<span>/ visit</span></p>
                    <p style="color:var(--text-muted);font-size:.92rem">Includes full examination, oral cancer screening and treatment plan. Cleanings from £65.</p>
                </div>
                <div class="widget widget--cta">
                    <h3 class="widget__title">Book This Service</h3>
                    <p>Ready to get started? Reserve your appointment in under a minute.</p>
                    <a href="appointment.html" class="btn btn--primary btn--block">Book Appointment</a>
                </div>
                <div class="widget">
                    <h3 class="widget__title">Need Help?</h3>
                    <p style="color:var(--text-muted)"><strong>Call us:</strong><br><a href="tel:+447908712026" style="color:var(--primary);font-weight:700">+44 7908 712 026</a></p>
                    <p style="color:var(--text-muted)"><strong>Email:</strong><br><a href="mailto:hello@toothwise.com" style="color:var(--primary);font-weight:700">hello@toothwise.com</a></p>
                </div>
            </aside>
        </div>
    </section>
    <section class="section section--gray">
        <div class="container">
            {section_head("Related", "Related Services", "Explore other treatments that pair well with your general dental care.")}
            <div class="services__grid">{related}</div>
        </div>
    </section>
    {cta_band("Time For Your Next Check-Up?", "Keep your smile healthy with a gentle, thorough general dentistry appointment.")}'''
page("service-details.html", "General Dentistry | ToothWise Dental Clinic",
     "Comprehensive general dentistry at ToothWise — exams, cleanings, fillings and preventive care. Learn about the benefits, procedure, FAQs and pricing.",
     "service-details", service_details_body)

# ======================================================================
# PAGE: doctors.html
# ======================================================================
doctors_body = banner("Our Doctors", [("Home","index.html"),("Doctors",None)]) + f'''    <section class="section">
        <div class="container">
            {section_head("Expert Dental Team", "Meet The Specialists Behind Your Smile", "Every ToothWise dentist combines deep expertise with a genuinely gentle touch. Click any profile to learn more.")}
            <div class="doctors__grid">{"".join(doctor_card(*d) for d in DOCTORS)}</div>
        </div>
    </section>
    {stats}
    {cta_band("Meet Your Dentist In Person", "Book a consultation with the specialist of your choice and start your journey to a healthier smile.")}'''
page("doctors.html", "Our Doctors | ToothWise Dental Clinic",
     "Meet the expert ToothWise dental team — specialists in oral surgery, endodontics, implantology and cosmetic dentistry, all dedicated to gentle care.",
     "doctors", doctors_body)

# ======================================================================
# PAGE: doctor-details.html  (Dr. Ruth Miller)
# ======================================================================
other_docs = "".join(doctor_card(*d) for d in DOCTORS[1:4])
doctor_details_body = banner("Doctor Profile", [("Home","index.html"),("Doctors","doctors.html"),("Dr. Ruth Miller",None)]) + f'''    <section class="section">
        <div class="container doctor-profile">
            <div class="reveal">
                <div class="doctor-profile__media">
                    <img src="assets/images/doctor1.jpg" alt="Portrait of Dr. Ruth Miller" />
                    <div class="doctor-profile__social">
                        <a href="https://facebook.com" aria-label="Dr. Ruth Miller on Facebook">{IC["fb"]}</a>
                        <a href="https://twitter.com" aria-label="Dr. Ruth Miller on Twitter">{IC["tw"]}</a>
                        <a href="https://linkedin.com" aria-label="Dr. Ruth Miller on LinkedIn">{IC["in"]}</a>
                    </div>
                </div>
                <div class="widget" style="margin-top:26px">
                    <h3 class="widget__title">Working Hours</h3>
                    <table class="hours-table"><tbody>
                        <tr><td>Monday – Thursday</td><td>9:00am – 5:00pm</td></tr>
                        <tr><td>Friday</td><td>9:00am – 3:00pm</td></tr>
                        <tr><td>Saturday</td><td>By appointment</td></tr>
                        <tr><td>Sunday</td><td>Closed</td></tr>
                    </tbody></table>
                    <a href="appointment.html" class="btn btn--primary btn--block" style="margin-top:18px">Book With Dr. Miller</a>
                </div>
            </div>
            <div class="article reveal">
                <span class="badge">Oral &amp; Maxillofacial Surgery</span>
                <h1 class="mt-0">Dr. Ruth Miller</h1>
                <span class="doctor-profile__role">Lead Oral Surgeon &amp; Co-Founder</span>
                <p>Dr. Ruth Miller is one of ToothWise's founding partners and leads our surgical team. With over eighteen years of clinical experience, she is renowned for turning complex extractions and surgical cases into calm, comfortable experiences for even the most anxious patients.</p>
                <p>Her patient-first philosophy — take the time, explain everything, never rush — has shaped the culture of the entire clinic.</p>
                <h2>Education</h2>
                <ul class="ticks">
                    <li>{IC["cap"]}<span>BDS, Bachelor of Dental Surgery — King's College London</span></li>
                    <li>{IC["cap"]}<span>MDS, Oral &amp; Maxillofacial Surgery — University of Manchester</span></li>
                    <li>{IC["cap"]}<span>Fellowship in Advanced Surgical Dentistry — Royal College of Surgeons</span></li>
                </ul>
                <h2>Certifications</h2>
                <ul class="ticks">
                    <li>{IC["award"]}<span>Member, General Dental Council (GDC Registered)</span></li>
                    <li>{IC["award"]}<span>Certified in IV &amp; Conscious Sedation Dentistry</span></li>
                    <li>{IC["award"]}<span>Advanced Life Support (Dental) Certified</span></li>
                </ul>
                <h2>Specializations</h2>
                <div class="skill"><div class="skill__head"><span>Surgical Extractions</span><span>98%</span></div><div class="skill__bar"><span class="skill__fill" data-level="98"></span></div></div>
                <div class="skill"><div class="skill__head"><span>Wisdom Teeth Removal</span><span>95%</span></div><div class="skill__bar"><span class="skill__fill" data-level="95"></span></div></div>
                <div class="skill"><div class="skill__head"><span>Bone Grafting</span><span>90%</span></div><div class="skill__bar"><span class="skill__fill" data-level="90"></span></div></div>
                <div class="skill"><div class="skill__head"><span>Sedation Dentistry</span><span>93%</span></div><div class="skill__bar"><span class="skill__fill" data-level="93"></span></div></div>
                <h2>Experience</h2>
                <ul class="info-grid">
                    <li>{IC["clock"]}<div><strong>18+ Years</strong><span>Clinical practice</span></div></li>
                    <li>{IC["users"]}<div><strong>6,000+</strong><span>Successful procedures</span></div></li>
                    <li>{IC["award"]}<div><strong>9 Awards</strong><span>For surgical excellence</span></div></li>
                    <li>{IC["smile"]}<div><strong>Founding Partner</strong><span>ToothWise, since 2008</span></div></li>
                </ul>
            </div>
        </div>
    </section>
    <section class="section section--gray">
        <div class="container">
            {section_head("The Team", "Other Specialists", "Discover more of the dedicated dentists caring for your family at ToothWise.")}
            <div class="doctors__grid">{other_docs}</div>
        </div>
    </section>
    {cta_band("Book An Appointment With Dr. Miller", "Reserve a consultation with our lead oral surgeon and experience truly gentle surgical care.")}'''
page("doctor-details.html", "Dr. Ruth Miller | ToothWise Dental Clinic",
     "Meet Dr. Ruth Miller, lead oral surgeon at ToothWise — her biography, education, certifications, specializations, experience and working hours.",
     "doctor-details", doctor_details_body)

# ======================================================================
# PAGE: gallery.html
# ======================================================================
GAL = [
    ("gallery1.jpg", "clinic", "Modern ToothWise dental treatment room"),
    ("gallery2.jpg", "team", "Dental team performing a procedure"),
    ("gallery3.jpg", "equipment", "Sterilized dental instruments on a tray"),
    ("gallery4.jpg", "patients", "Happy patient smiling after treatment"),
    ("about2.jpg", "team", "Dentist examining a patient"),
    ("about3.jpg", "clinic", "Consultation with a dental model"),
    ("about1.jpg", "team", "Two dentists in the clinic"),
    ("hero.jpg", "clinic", "The ToothWise dental team at work"),
    ("blog1.jpg", "patients", "Bright, healthy smile after treatment"),
]
def gal_item(img, cat, alt):
    return f'''<button class="gallery__item reveal" data-category="{cat}" data-full="assets/images/{img}" aria-label="Open image: {alt}">
        <img src="assets/images/{img}" alt="{alt}" loading="lazy" /><span class="gallery__zoom" aria-hidden="true">+</span>
    </button>'''
gallery_body = banner("Gallery", [("Home","index.html"),("Gallery",None)]) + f'''    <section class="section">
        <div class="container">
            {section_head("Our Clinic", "A Look Inside ToothWise", "Step into a calm, spotless and thoughtfully designed space built entirely around your comfort. Click any image to enlarge.")}
            <div class="filters reveal" data-filter-group data-filter-target=".gallery__item">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="clinic">Clinic</button>
                <button class="filter-btn" data-filter="team">Our Team</button>
                <button class="filter-btn" data-filter="equipment">Equipment</button>
                <button class="filter-btn" data-filter="patients">Patients</button>
            </div>
            <div class="gallery__grid">{"".join(gal_item(*g) for g in GAL)}</div>
        </div>
    </section>
    {cta_band("Come And See Us For Yourself", "Photos only tell part of the story. Book a visit and experience the ToothWise difference in person.")}'''
page("gallery.html", "Gallery | ToothWise Dental Clinic",
     "Take a visual tour of the ToothWise clinic — our modern treatment rooms, dedicated team, advanced equipment and happy patients.",
     "gallery", gallery_body, lightbox=True)

# ======================================================================
# PAGE: testimonials.html
# ======================================================================
REVIEWS = [
    ("implants", 5, "I was terrified of dentists my whole life until I found ToothWise. My implants look and feel completely natural — I finally smile in photos again.", "Sarah Jennings", "Implant Patient"),
    ("family", 5, "My kids used to dread check-ups. Now they beg to go! The pediatric team makes every visit feel like an adventure.", "Emily Roberts", "Parent of Two"),
    ("cosmetic", 5, "The teeth whitening results blew me away — years of coffee stains gone in a single appointment. Transparent pricing too.", "Daniel Cooper", "Cosmetic Patient"),
    ("cosmetic", 5, "My veneers are flawless. Dr. Ettore listened to exactly what I wanted and the result looks completely natural.", "Priya Sharma", "Veneers Patient"),
    ("implants", 4, "A calm, professional experience from start to finish. The surgery was painless and healing was quicker than I expected.", "Marcus Bell", "Oral Surgery Patient"),
    ("family", 5, "Three generations of my family are cared for here. Friendly reception, spotless clinic and never a long wait.", "Grace O'Neill", "Long-time Patient"),
    ("general", 5, "I chipped a tooth on a Sunday and they saw me within the hour. The 24/7 emergency service is a lifesaver.", "Tom Fletcher", "Emergency Patient"),
    ("general", 5, "Honest advice, no upselling, and they explain everything clearly. Exactly what you want from a dentist.", "Aisha Khan", "General Dentistry Patient"),
    ("cosmetic", 4, "Fantastic orthodontic care. My clear aligners were comfortable and the results speak for themselves.", "James Whitfield", "Orthodontics Patient"),
]
def review_card(cat, rating, text, name, role):
    return f'''<article class="review-card reveal" data-category="{cat}">
        {stars(rating)}
        <p>"{text}"</p>
        <footer class="testimonial__author"><img src="assets/images/{DOCTORS[hash(name)%4][0]}" alt="Photo of {name}" loading="lazy" style="width:52px;height:52px" /><div><cite>{name}</cite><span>{role}</span></div></footer>
    </article>'''
testimonials_body = banner("Testimonials", [("Home","index.html"),("Testimonials",None)]) + f'''    <section class="section">
        <div class="container">
            {section_head("Happy Patients", "Trusted By Thousands Of Smiles", "Real reviews from real patients. Filter by treatment type to see what our patients say.")}
            <div class="filters reveal" data-filter-group data-filter-target=".review-card">
                <button class="filter-btn active" data-filter="all">All Reviews</button>
                <button class="filter-btn" data-filter="general">General</button>
                <button class="filter-btn" data-filter="cosmetic">Cosmetic</button>
                <button class="filter-btn" data-filter="implants">Implants</button>
                <button class="filter-btn" data-filter="family">Family</button>
            </div>
            <div class="testimonials-grid">{"".join(review_card(*r) for r in REVIEWS)}</div>
        </div>
    </section>
    {stats}
    {cta_band("Become Our Next Happy Patient", "Join thousands of people who trust ToothWise with their smiles. Book your first visit today.")}'''
page("testimonials.html", "Testimonials | ToothWise Dental Clinic",
     "Read genuine patient reviews of ToothWise Dental Clinic. Filter by treatment — general, cosmetic, implants and family dentistry.",
     "testimonials", testimonials_body)

# ======================================================================
# PAGE: faq.html
# ======================================================================
faq_items_html = "".join(faq_item(c, q, a, filterable=True) for c, q, a in FAQS)
faq_body = banner("FAQ", [("Home","index.html"),("FAQ",None)]) + f'''    <section class="section">
        <div class="container">
            {section_head("FAQ", "Frequently Asked Questions", "Everything you need to know before your first visit. Search or filter to find your answer quickly.")}
            <div class="faq__list reveal" style="margin-bottom:24px">
                <div class="widget__search" role="search">
                    <label for="faq-search" class="sr-only">Search FAQs</label>
                    <input type="search" id="faq-search" placeholder="Search questions…" />
                    <button type="button" aria-label="Search">{IC["search"]}</button>
                </div>
            </div>
            <div class="filters reveal" data-filter-group data-filter-target=".faq-item">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="General">General</button>
                <button class="filter-btn" data-filter="Treatments">Treatments</button>
                <button class="filter-btn" data-filter="Billing">Billing &amp; Insurance</button>
            </div>
            <div class="faq__list reveal">
                {faq_items_html}
                <p id="faq-empty" hidden style="text-align:center;color:var(--text-muted);padding:20px">No questions match your search. Try a different keyword.</p>
            </div>
        </div>
    </section>
    {cta_band("Still Have Questions?", "Our friendly team is always happy to help. Get in touch and we'll answer anything you need.", primary=("Contact Us","contact.html"), secondary=("Book Appointment","appointment.html"))}'''
page("faq.html", "FAQ | ToothWise Dental Clinic",
     "Answers to common questions about visiting ToothWise — appointments, treatments, pain, pricing, insurance and emergency dental care.",
     "faq", faq_body)

# ======================================================================
# PAGE: blog.html
# ======================================================================
EXTRA_BLOGS = [
    ("about3.jpg", "Orthodontics", "May 28, 2026", "2026-05-28", "Dr. Ruth Miller",
     "Braces vs Clear Aligners: Which Is Right For You?",
     "Both straighten teeth beautifully, but they suit different lifestyles. We compare comfort, cost, treatment time and results."),
    ("gallery2.jpg", "Emergency", "May 9, 2026", "2026-05-09", "Dr. Alex Turner",
     "What To Do When A Tooth Gets Knocked Out",
     "The first 30 minutes matter most. Follow these simple steps to give a knocked-out tooth the best chance of being saved."),
    ("about2.jpg", "Kids", "April 22, 2026", "2026-04-22", "Dr. Basilio Ettore",
     "Making Dental Visits Fun For Your Children",
     "A few simple tricks can turn dental anxiety into excitement. Here's how we help kids look forward to the dentist."),
]
ALL_BLOGS = BLOGS + EXTRA_BLOGS
blog_body = banner("Our Blog", [("Home","index.html"),("Blog",None)]) + f'''    <section class="section">
        <div class="container">
            {section_head("Latest News", "Insights &amp; Articles", "Practical tips, expert advice and the latest in dental health from the ToothWise team.")}
            <div class="blog__grid">{"".join(blog_card(*b) for b in ALL_BLOGS)}</div>
        </div>
    </section>
    {cta_band("Have A Question We Haven't Covered?", "Our dentists love to help. Book a consultation and get expert advice tailored to you.")}'''
page("blog.html", "Blog | ToothWise Dental Clinic",
     "Dental health tips, treatment guides and clinic news from the ToothWise team — covering cosmetic, preventive, orthodontic and emergency care.",
     "blog", blog_body)

# ======================================================================
# PAGE: blog-single.html
# ======================================================================
recent = "".join(f'''<li><div class="recent-post"><img src="assets/images/{b[0]}" alt="{b[5]}" loading="lazy" /><div><h4><a href="blog-single.html">{b[5]}</a></h4><span>{b[2]}</span></div></div></li>''' for b in ALL_BLOGS[:4])
cats = "".join(f'<li><a href="blog.html">{c} <span>({n})</span></a></li>' for c, n in [("Cosmetic","8"),("Prevention","6"),("Implants","5"),("Orthodontics","4"),("Emergency","3"),("Kids","4")])
tags = "".join(f'<a href="blog.html">{t}</a>' for t in ["Whitening","Implants","Braces","Hygiene","Kids","Emergency","Veneers","Cleaning"])
related_posts = "".join(blog_card(*b) for b in ALL_BLOGS[1:4])
def comment(initial, name, date, text, reply=False):
    cls = " comment--reply" if reply else ""
    return f'''<div class="comment{cls}"><div class="comment__avatar" aria-hidden="true">{initial}</div><div><div class="comment__head"><h4>{name}</h4><time>{date}</time></div><p>{text}</p><a href="#comment-form" class="link-more">Reply</a></div></div>'''
blog_single_body = banner("Blog Details", [("Home","index.html"),("Blog","blog.html"),("Article",None)]) + f'''    <section class="section">
        <div class="container layout">
            <article class="article reveal">
                <img src="assets/images/blog1.jpg" alt="A bright, healthy white smile" class="article__img" loading="lazy" />
                <div class="blog-card__meta" style="margin-bottom:14px"><span class="blog-card__cat" style="position:static">Cosmetic</span><time datetime="2026-07-24">July 24, 2026</time><span>By Dr. Basilio Ettore</span></div>
                <h1 class="mt-0">5 Simple Habits For A Brighter, Whiter Smile</h1>
                <p>A radiant smile doesn't only come from the dentist's chair — it's built and maintained through small, consistent daily habits. While professional whitening delivers dramatic results, the way you care for your teeth in between visits determines how long that brightness lasts.</p>
                <h2>1. Rethink Your Brushing Routine</h2>
                <p>Brushing twice a day is essential, but technique matters more than force. Use a soft-bristled brush and fluoride toothpaste, and give each session a full two minutes. Brushing too hard can wear enamel and actually make teeth look more yellow over time.</p>
                <h2>2. Watch The Staining Culprits</h2>
                <p>Coffee, red wine, tea and dark berries are the biggest offenders when it comes to surface stains. You don't have to give them up — simply rinse with water afterward, or sip through a straw where practical.</p>
                <blockquote>"The best whitening result is the one you protect. Great home habits make a professional treatment last twice as long." — Dr. Basilio Ettore</blockquote>
                <h2>3. Don't Skip Your Cleanings</h2>
                <p>Professional cleanings remove the hardened tartar and deep stains that brushing simply can't reach. A twice-yearly hygiene visit keeps your smile brighter and your gums healthier.</p>
                <ul class="ticks">
                    <li>{IC["tick"]}<span>Drink plenty of water throughout the day.</span></li>
                    <li>{IC["tick"]}<span>Eat crunchy fruits and vegetables that naturally clean teeth.</span></li>
                    <li>{IC["tick"]}<span>Avoid tobacco, the number one cause of stubborn staining.</span></li>
                </ul>
                <p>Combine these habits with a professional whitening treatment at ToothWise and you'll enjoy a confident, camera-ready smile all year round.</p>

                <div class="comments">
                    <h2>Comments (3)</h2>
                    {comment("LM","Laura Mitchell","July 25, 2026","This was so helpful — I had no idea brushing too hard could make teeth look yellower. Booking a cleaning now!")}
                    {comment("TW","ToothWise Team","July 25, 2026","So glad it helped, Laura! We'll see you soon for your cleaning. 😊", reply=True)}
                    {comment("RG","Ravi Gupta","July 26, 2026","The straw tip is genius. Already noticing fewer coffee stains this week.")}
                </div>

                <div class="widget" id="comment-form" style="margin-top:36px">
                    <h3 class="widget__title">Leave A Comment</h3>
                    <form class="contact-form" onsubmit="return false">
                        <div class="form-row">
                            <div class="form-group"><label for="c-name">Name</label><input type="text" id="c-name" name="c-name" placeholder="Your name" /></div>
                            <div class="form-group"><label for="c-email">Email</label><input type="email" id="c-email" name="c-email" placeholder="Your email" /></div>
                        </div>
                        <div class="form-group"><label for="c-msg">Comment</label><textarea id="c-msg" name="c-msg" rows="4" placeholder="Share your thoughts…"></textarea></div>
                        <button type="submit" class="btn btn--primary">Post Comment</button>
                    </form>
                </div>
            </article>

            <aside class="sidebar reveal">
                <div class="widget"><h3 class="widget__title">Search</h3>
                    <div class="widget__search"><label for="blog-search" class="sr-only">Search blog</label><input type="search" id="blog-search" placeholder="Search articles…" /><button type="button" aria-label="Search">{IC["search"]}</button></div>
                </div>
                <div class="widget"><h3 class="widget__title">Categories</h3><ul class="cat-list">{cats}</ul></div>
                <div class="widget"><h3 class="widget__title">Recent Posts</h3><ul class="recent-list">{recent}</ul></div>
                <div class="widget"><h3 class="widget__title">Popular Tags</h3><div class="tag-cloud">{tags}</div></div>
                <div class="widget widget--cta"><h3 class="widget__title">Book A Visit</h3><p>Ready for a brighter smile? Our team is here to help.</p><a href="appointment.html" class="btn btn--primary btn--block">Book Appointment</a></div>
            </aside>
        </div>
    </section>
    <section class="section section--gray">
        <div class="container">
            {section_head("Keep Reading", "Related Articles", "More expert insights to help you care for your smile.")}
            <div class="blog__grid">{related_posts}</div>
        </div>
    </section>'''
page("blog-single.html", "5 Simple Habits For A Brighter Smile | ToothWise Blog",
     "Discover five simple daily habits that keep your smile brighter and whiter for longer, with expert advice from the ToothWise dental team.",
     "blog-single", blog_single_body)

# ======================================================================
# PAGE: pricing.html
# ======================================================================
def price_list(items):
    # items: list of (text, included_bool)
    out = ""
    for text, inc in items:
        cls = "" if inc else " class=\"off\""
        out += f'<li{cls}>{IC["tick"]}<span>{text}</span></li>'
    return out
def price_card(name, desc, price, period, items, popular=False, cta="Choose Plan"):
    tag = '<span class="price-card__tag">Most Popular</span>' if popular else ""
    cls = "price-card price-card--popular" if popular else "price-card"
    btn = "btn--primary" if popular else "btn--dark"
    return f'''<article class="{cls} reveal">{tag}
        <h3>{name}</h3><p class="price-card__desc">{desc}</p>
        <div class="price-card__price">{price}<span>/ {period}</span></div>
        <ul class="price-card__list">{price_list(items)}</ul>
        <a href="appointment.html" class="btn {btn} btn--block">{cta}</a>
    </article>'''
pricing_body = banner("Pricing", [("Home","index.html"),("Pricing",None)]) + f'''    <section class="section">
        <div class="container">
            {section_head("Transparent Pricing", "Simple, Honest Dental Plans", "No hidden fees, ever. Choose a care plan that fits your needs, or pay per treatment — the choice is always yours.")}
            <div class="pricing__grid">
                {price_card("Essential Care", "Perfect for individuals who want to stay on top of their oral health.", "£19", "month",
                    [("2 dental check-ups per year", True),("1 professional cleaning per year", True),("Annual digital X-rays", True),("10% off treatments", True),("Emergency priority booking", False),("Free whitening consultation", False)])}
                {price_card("Family Plus", "Our most popular plan — complete cover for the whole family.", "£39", "month",
                    [("4 dental check-ups per year", True),("2 professional cleanings per year", True),("Digital X-rays included", True),("20% off all treatments", True),("Emergency priority booking", True),("Free whitening consultation", False)], popular=True)}
                {price_card("Premium Smile", "The ultimate care package with cosmetic perks included.", "£69", "month",
                    [("Unlimited check-ups", True),("4 professional cleanings per year", True),("All X-rays &amp; imaging included", True),("30% off all treatments", True),("24/7 emergency priority", True),("Free annual whitening session", True)])}
            </div>
        </div>
    </section>
    <section class="section section--gray">
        <div class="container">
            {section_head("Compare", "Compare Our Plans", "See exactly what's included in each membership at a glance.")}
            <div class="compare reveal">
                <table>
                    <thead><tr><th>Feature</th><th>Essential</th><th>Family Plus</th><th>Premium</th></tr></thead>
                    <tbody>
                        <tr><td>Annual Check-ups</td><td>2</td><td>4</td><td>Unlimited</td></tr>
                        <tr><td>Professional Cleanings</td><td>1</td><td>2</td><td>4</td></tr>
                        <tr><td>X-rays &amp; Imaging</td><td class="yes">✔</td><td class="yes">✔</td><td class="yes">✔</td></tr>
                        <tr><td>Treatment Discount</td><td>10%</td><td>20%</td><td>30%</td></tr>
                        <tr><td>Emergency Priority</td><td class="no">—</td><td class="yes">✔</td><td class="yes">✔</td></tr>
                        <tr><td>Free Whitening Session</td><td class="no">—</td><td class="no">—</td><td class="yes">✔</td></tr>
                        <tr><td>Monthly Price</td><td>£19</td><td>£39</td><td>£69</td></tr>
                    </tbody>
                </table>
            </div>
            <p class="text-center" style="color:var(--text-muted);margin-top:24px">Prefer to pay as you go? Individual treatments start from just £49. <a href="contact.html" class="link-more" style="display:inline-flex">Ask us for a quote &rarr;</a></p>
        </div>
    </section>
    {cta_band("Join A Plan &amp; Start Saving", "Membership means healthier smiles and lower bills. Sign up today or ask our team which plan suits you best.")}'''
page("pricing.html", "Pricing &amp; Plans | ToothWise Dental Clinic",
     "Simple, transparent dental pricing at ToothWise. Compare our Essential, Family Plus and Premium membership plans, or pay per treatment.",
     "pricing", pricing_body)

# ======================================================================
# PAGE: appointment.html
# ======================================================================
service_options = "".join(f'<option value="{t}">{t}</option>' for t, _ in SERVICES)
doctor_options = "".join(f'<option value="{d[1]}">{d[1]} — {d[2]}</option>' for d in DOCTORS)
appointment_body = banner("Book Appointment", [("Home","index.html"),("Appointment",None)]) + f'''    <section class="section">
        <div class="container">
            {section_head("Get Started", "Book Your Appointment", "Fill in the form below and our team will confirm your booking within one business day. For emergencies, please call us directly.")}
            <form class="appointment-form reveal" id="appointment-form" novalidate>
                <div class="form-row">
                    <div class="form-group"><label for="name">Full Name *</label><input type="text" id="name" name="name" placeholder="Jane Doe" required /><small class="form-error" data-for="name"></small></div>
                    <div class="form-group"><label for="email">Email Address *</label><input type="email" id="email" name="email" placeholder="jane@email.com" required /><small class="form-error" data-for="email"></small></div>
                </div>
                <div class="form-grid-3">
                    <div class="form-group"><label for="phone">Phone Number *</label><input type="tel" id="phone" name="phone" placeholder="+44 7908 712 026" required /><small class="form-error" data-for="phone"></small></div>
                    <div class="form-group"><label for="service">Service</label><select id="service" name="service">{service_options}</select></div>
                    <div class="form-group"><label for="doctor">Preferred Doctor</label><select id="doctor" name="doctor"><option value="No preference">No preference</option>{doctor_options}</select></div>
                </div>
                <div class="form-row">
                    <div class="form-group"><label for="date">Preferred Date *</label><input type="date" id="date" name="date" required /><small class="form-error" data-for="date"></small></div>
                    <div class="form-group"><label for="time">Preferred Time *</label>
                        <select id="time" name="time" required>
                            <option value="">Select a time…</option>
                            <option>09:00 – 10:00</option><option>10:00 – 11:00</option><option>11:00 – 12:00</option>
                            <option>13:00 – 14:00</option><option>14:00 – 15:00</option><option>15:00 – 16:00</option><option>16:00 – 17:00</option>
                        </select><small class="form-error" data-for="time"></small></div>
                </div>
                <div class="form-group"><label for="message">Additional Notes</label><textarea id="message" name="message" rows="4" placeholder="Tell us anything that will help us prepare for your visit…"></textarea></div>
                <button type="submit" class="btn btn--primary btn--lg btn--block">Request Appointment</button>
                <p class="form-success" id="appointment-success" role="status" hidden>Thank you! Your appointment request has been received — we'll confirm within one business day.</p>
            </form>
        </div>
    </section>
    <section class="stats" aria-label="Contact"><div class="stats__overlay"></div>
        <div class="container stats__grid" style="grid-template-columns:repeat(3,1fr)">
            <div class="stat reveal"><span class="stat__num" style="font-size:1.6rem">Call Us</span><span class="stat__label"><a href="tel:+447908712026" style="color:#fff">+44 7908 712 026</a></span></div>
            <div class="stat reveal"><span class="stat__num" style="font-size:1.6rem">Email</span><span class="stat__label"><a href="mailto:hello@toothwise.com" style="color:#fff">hello@toothwise.com</a></span></div>
            <div class="stat reveal"><span class="stat__num" style="font-size:1.6rem">Emergency</span><span class="stat__label">Available 24/7</span></div>
        </div>
    </section>'''
page("appointment.html", "Book An Appointment | ToothWise Dental Clinic",
     "Book your dental appointment online at ToothWise. Choose your service, preferred doctor, date and time — we'll confirm within one business day.",
     "appointment", appointment_body)

# ======================================================================
# PAGE: contact.html
# ======================================================================
contact_body = banner("Contact Us", [("Home","index.html"),("Contact",None)]) + f'''    <section class="section">
        <div class="container">
            {section_head("Get In Touch", "We'd Love To Hear From You", "Have a question or ready to book? Reach out and our friendly team will get back to you within one business day.")}
            <div class="contact__grid">
                <div class="contact__info reveal">
                    <ul class="contact__list">
                        <li><span class="contact__icon">{IC["pin"]}</span><div><h3>Visit Us</h3><p>221B Baker Street, London, England</p></div></li>
                        <li><span class="contact__icon">{IC["phone"]}</span><div><h3>Call Us</h3><p><a href="tel:+447908712026">+44 7908 712 026</a></p></div></li>
                        <li><span class="contact__icon">{IC["mail"]}</span><div><h3>Email Us</h3><p><a href="mailto:hello@toothwise.com">hello@toothwise.com</a></p></div></li>
                        <li><span class="contact__icon">{IC["plus"]}</span><div><h3>Emergency (24/7)</h3><p><a href="tel:+447908999111">+44 7908 999 111</a></p></div></li>
                        <li><span class="contact__icon">{IC["clock"]}</span><div><h3>Business Hours</h3><p>Mon–Fri: 9:00am – 5:00pm<br>Saturday: 9:00am – 2:00pm<br>Sunday: Emergency only</p></div></li>
                    </ul>
                    <div class="contact__map" role="img" aria-label="Map showing ToothWise clinic location">
                        <iframe title="ToothWise clinic location map" src="https://www.google.com/maps?q=Baker+Street,+London&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                </div>
                <div class="contact__form-wrap reveal">
                    <form class="contact-form" id="contact-form" novalidate>
                        <div class="form-row">
                            <div class="form-group"><label for="name">Full Name</label><input type="text" id="name" name="name" placeholder="Jane Doe" required /><small class="form-error" data-for="name"></small></div>
                            <div class="form-group"><label for="email">Email Address</label><input type="email" id="email" name="email" placeholder="jane@email.com" required /><small class="form-error" data-for="email"></small></div>
                        </div>
                        <div class="form-row">
                            <div class="form-group"><label for="phone">Phone Number</label><input type="tel" id="phone" name="phone" placeholder="+44 7908 712 026" required /><small class="form-error" data-for="phone"></small></div>
                            <div class="form-group"><label for="subject">Subject</label><input type="text" id="subject" name="subject" placeholder="How can we help?" /></div>
                        </div>
                        <div class="form-group"><label for="message">Message</label><textarea id="message" name="message" rows="5" placeholder="Tell us how we can help…" required></textarea><small class="form-error" data-for="message"></small></div>
                        <button type="submit" class="btn btn--primary btn--lg btn--block">Send Message</button>
                        <p class="form-success" id="form-success" role="status" hidden>Thank you! Your message has been received — we'll be in touch shortly.</p>
                    </form>
                </div>
            </div>
        </div>
    </section>
    {cta_band("Prefer To Book Right Away?", "Skip the wait and reserve your appointment online in under a minute.", primary=("Book Appointment","appointment.html"), secondary=("View Services","services.html"))}'''
page("contact.html", "Contact Us | ToothWise Dental Clinic",
     "Contact ToothWise Dental Clinic — address, phone, email, business hours and 24/7 emergency line. Send us a message or find us on the map.",
     "contact", contact_body)

# ======================================================================
# PAGE: privacy-policy.html
# ======================================================================
privacy_body = banner("Privacy Policy", [("Home","index.html"),("Privacy Policy",None)]) + f'''    <section class="section">
        <div class="container" style="max-width:860px">
            <div class="legal article reveal">
                <p class="updated">Last updated: 7 August 2026</p>
                <p>At ToothWise Dental Clinic ("we", "us", "our"), your privacy matters as much as your smile. This Privacy Policy explains how we collect, use and protect your personal information when you visit our website or attend our clinic.</p>
                <h2>Information We Collect</h2>
                <p>We may collect the following information when you interact with us:</p>
                <ul>
                    <li>Contact details such as your name, email address and phone number.</li>
                    <li>Appointment details, including preferred dates, services and doctor preferences.</li>
                    <li>Medical and dental history necessary to provide safe, effective treatment.</li>
                    <li>Technical data such as browser type and pages visited, collected via standard analytics.</li>
                </ul>
                <h2>How We Use Your Information</h2>
                <ul>
                    <li>To schedule, confirm and manage your appointments.</li>
                    <li>To provide dental care and maintain accurate treatment records.</li>
                    <li>To respond to your enquiries and send appointment reminders.</li>
                    <li>To improve our website and services.</li>
                </ul>
                <h2>Data Protection</h2>
                <p>We apply strict organisational and technical safeguards to protect your data against unauthorised access, loss or misuse. Access to patient records is limited to authorised clinical staff only.</p>
                <h2>Your Rights</h2>
                <p>You have the right to access, correct or request deletion of your personal data, and to withdraw consent to marketing communications at any time. To exercise these rights, contact us at <a href="mailto:hello@toothwise.com">hello@toothwise.com</a>.</p>
                <h2>Cookies</h2>
                <p>Our website uses essential and analytics cookies to improve your browsing experience. You can control cookies through your browser settings at any time.</p>
                <h2>Contact Us</h2>
                <p>If you have any questions about this Privacy Policy, please contact us at <a href="mailto:hello@toothwise.com">hello@toothwise.com</a> or call <a href="tel:+447908712026">+44 7908 712 026</a>.</p>
            </div>
        </div>
    </section>'''
page("privacy-policy.html", "Privacy Policy | ToothWise Dental Clinic",
     "Read the ToothWise Dental Clinic Privacy Policy — how we collect, use and protect your personal and medical information.",
     "privacy", privacy_body)

# ======================================================================
# PAGE: terms.html
# ======================================================================
terms_body = banner("Terms of Service", [("Home","index.html"),("Terms of Service",None)]) + f'''    <section class="section">
        <div class="container" style="max-width:860px">
            <div class="legal article reveal">
                <p class="updated">Last updated: 7 August 2026</p>
                <p>Welcome to ToothWise Dental Clinic. By accessing our website or using our services, you agree to the following terms and conditions. Please read them carefully.</p>
                <h2>Use Of Our Website</h2>
                <p>The content on this website is provided for general information only and does not constitute medical or dental advice. Always consult a qualified dentist for guidance specific to your situation.</p>
                <h2>Appointments &amp; Cancellations</h2>
                <ul>
                    <li>Appointment requests submitted online are confirmed subject to availability.</li>
                    <li>We kindly ask for at least 24 hours' notice to cancel or reschedule an appointment.</li>
                    <li>Repeated missed appointments without notice may incur a fee.</li>
                </ul>
                <h2>Payments</h2>
                <p>Payment is due at the time of treatment unless otherwise agreed. We accept major cards and offer approved payment plans on eligible treatments. All prices are inclusive of applicable taxes.</p>
                <h2>Treatment Consent</h2>
                <p>All treatments are carried out only after informed consent. Our dentists will explain the procedure, risks, benefits and costs before any treatment begins.</p>
                <h2>Limitation Of Liability</h2>
                <p>While we strive for the highest standards of care, ToothWise is not liable for outcomes arising from information used from this website without professional consultation.</p>
                <h2>Changes To These Terms</h2>
                <p>We may update these terms from time to time. Continued use of our website and services constitutes acceptance of the current terms.</p>
                <h2>Contact Us</h2>
                <p>Questions about these Terms? Email <a href="mailto:hello@toothwise.com">hello@toothwise.com</a> or call <a href="tel:+447908712026">+44 7908 712 026</a>.</p>
            </div>
        </div>
    </section>'''
page("terms.html", "Terms of Service | ToothWise Dental Clinic",
     "The Terms of Service for ToothWise Dental Clinic — website use, appointments, cancellations, payments and treatment consent.",
     "terms", terms_body)

# ======================================================================
# PAGE: 404.html
# ======================================================================
notfound_body = f'''    <section class="notfound">
        <div class="container">
            <div class="reveal">
                <div class="notfound__code">404</div>
                <h1>Oops! This Page Took A Wrong Turn</h1>
                <p>The page you're looking for doesn't exist or may have moved. Don't worry — let's get you back to a healthy smile.</p>
                <div class="hero__actions" style="justify-content:center">
                    <a href="index.html" class="btn btn--primary btn--lg">Back To Home</a>
                    <a href="contact.html" class="btn btn--dark btn--lg">Contact Us</a>
                </div>
            </div>
        </div>
    </section>'''
page("404.html", "Page Not Found | ToothWise Dental Clinic",
     "The page you're looking for could not be found. Return to the ToothWise homepage or contact our team.",
     "404", notfound_body)

print("\\nALL PAGES BUILT")

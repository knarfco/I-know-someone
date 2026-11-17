"""Legal and compliance pages. Plain English. [[...]] = facts to confirm with the company.
Have the company's attorney review before launch.
"""

EFFECTIVE = "[[Month Day, 2026]]"

LEGAL = [
    {
        "slug": "privacy",
        "title": "Privacy Policy",
        "lead": "What information we collect, how we use it, and the choices you have.",
        "sections": [
            ("Who we are", "<p>This website is operated by {name} (“we,” “us”). This policy explains how we handle information collected through this website, including our bid request form, service checklist, phone and email links, and text messages.</p>"),
            ("Information you give us", "<ul class=\"checks\"><li><b>Bid requests and contact forms:</b> your name, company or agency, phone number, email address, job location, project details, permit status, solicitation numbers and anything else you choose to send.</li><li><b>Service checklist:</b> your name and your selections.</li><li><b>Calls, emails and texts:</b> your phone number, email address and the content of your messages.</li><li><b>Photos or videos</b> you send us of a job site.</li></ul>"),
            ("Information collected automatically", "<p>Like most websites, our hosting provider records basic technical information when you visit: your IP address, browser and device type, the pages you view, the page that referred you and the date and time. When you submit a bid request, the form also records which page you first landed on and how you found us, so we know which parts of the site help people most.</p><p><b>Browser storage:</b> the site uses your browser's local storage to remember your service checklist answers and your first landing page during a visit. This information stays on your device unless you submit a form.</p><p><b>Analytics:</b> [[We use Google Analytics / no analytics — confirm]]. If analytics are used, they collect information about how visitors use the site in aggregate. You can block analytics cookies in your browser settings.</p>"),
            ("How we use information", "<ul class=\"checks\"><li>To respond to your request, prepare estimates and bids, and do the work you hire us for.</li><li>To contact you by phone, email or text about your request.</li><li>To keep records required for contracts, permits, insurance and government reimbursement (such as FEMA documentation).</li><li>To improve the website and understand how people find us.</li><li>To protect against fraud, spam and misuse.</li></ul>"),
            ("How we share information", "<p>We <b>do not sell</b> your personal information. We share it only when needed to serve you:</p><ul class=\"checks\"><li><b>Partner contractors and specialists:</b> when your project needs a licensed partner (for example, a specialty trade or a crew closer to your site), we may share your project details and contact information with that partner so they can help with your request.</li><li><b>Service providers</b> who help us run the business, such as our website host, email and phone providers. They may use your information only to provide services to us.</li><li><b>Government agencies and prime contractors</b> when required by a contract, permit, reimbursement program or law.</li><li><b>Legal reasons:</b> to comply with law, respond to lawful requests, or protect our rights and safety.</li></ul><p><b>Mobile numbers and text messaging consent are never shared with or sold to third parties or affiliates for their marketing purposes.</b></p>"),
            ("Text messages", "<p>If you agree to receive text messages, we use your number only to communicate about your request or project. See our <a href=\"{text_terms}\">Text Messaging Terms</a>. Reply STOP at any time to opt out.</p>"),
            ("How long we keep information", "<p>We keep information as long as needed to respond to you, perform our work and meet legal, tax, contract and insurance record-keeping requirements. Public-contract records may be kept longer where public records laws require it.</p>"),
            ("Security", "<p>We use reasonable measures to protect information. No website or transmission over the internet is completely secure, so please do not send sensitive information such as bank account numbers or Social Security numbers through the website.</p>"),
            ("Children", "<p>This website is for businesses, agencies and property owners. It is not directed to children under 13, and we do not knowingly collect their information.</p>"),
            ("Your choices", "<ul class=\"checks\"><li>Ask to see, correct or delete the information you have given us, subject to records we must keep by law or contract.</li><li>Opt out of texts by replying STOP, and out of emails by asking us.</li><li>Clear your browser storage at any time to remove saved checklist answers.</li></ul>"),
            ("Changes to this policy", "<p>We may update this policy. The effective date below shows when it last changed.</p>"),
            ("Contact us", "<p>{name}<br>{address}<br>{city_state}<br>Phone: {phone}<br>Email: {email}</p>"),
        ],
    },
    {
        "slug": "terms",
        "title": "Terms of Use",
        "lead": "The rules for using this website.",
        "sections": [
            ("Agreement", "<p>By using this website, you agree to these Terms of Use. If you do not agree, please do not use the site.</p>"),
            ("General information only", "<p>Content on this website, including cost ranges, timelines, permit information and answers to common questions, is general information. It is <b>not a quote, bid, contract, or legal, engineering or environmental advice</b>. Every site is different, and rules vary by location and change over time. Always confirm permit requirements with the issuing agency.</p>"),
            ("Quotes and contracts", "<p>Prices and scope are set only in a written estimate, proposal or signed contract. Submitting a bid request does not create a contract or obligate either party.</p>"),
            ("Your submissions", "<p>When you send us information, photos or videos, you confirm you have the right to share them and that they are accurate to the best of your knowledge. You allow us to use them to respond to your request and perform the work. We will not publish photos of your property without your permission.</p>"),
            ("Our content", "<p>The text, photos, videos, logos and design of this website belong to {name} or its licensors and are protected by copyright and trademark law. You may view and share pages for personal or business evaluation, but you may not copy, modify or republish site content without written permission.</p>"),
            ("Acceptable use", "<p>Please do not misuse the site: no attempts to break security, send spam or malicious code, scrape content at scale, or submit false information.</p>"),
            ("Third-party links and video", "<p>The site links to and embeds third-party services such as YouTube and Google. Their own terms and privacy policies apply, and we are not responsible for their content.</p>"),
            ("Disclaimer", "<p>The website is provided “as is.” We work to keep it accurate and available but do not guarantee that it is error-free or uninterrupted.</p>"),
            ("Limitation of liability", "<p>To the fullest extent allowed by law, {name} is not liable for indirect, incidental or consequential damages arising from use of this website. Nothing in these terms limits obligations in a signed contract.</p>"),
            ("Governing law", "<p>These terms are governed by the laws of the State of Florida. Any dispute about the website will be handled in the courts of [[County]] County, Florida.</p>"),
            ("Changes", "<p>We may update these terms. The effective date below shows when they last changed.</p>"),
            ("Contact", "<p>Questions? Call {phone} or email {email}.</p>"),
        ],
    },
    {
        "slug": "accessibility",
        "title": "Accessibility Statement",
        "lead": "We want everyone to be able to use this website, including people who are blind, have low vision, are deaf or hard of hearing, or use a keyboard or assistive technology.",
        "sections": [
            ("Our commitment", "<p>{name} is committed to making this website accessible. Our goal is to conform to the <b>Web Content Accessibility Guidelines (WCAG) 2.1, Level AA</b>, the standard referenced under the Americans with Disabilities Act (ADA) and aligned with Section 508 of the Rehabilitation Act.</p>"),
            ("What we've done", "<ul class=\"checks\"><li>Text alternatives for meaningful images and a text label for the logo.</li><li>Clear page structure with headings, landmarks and a “Skip to content” link.</li><li>Full keyboard navigation, including menus, forms, the before-and-after slider and the service checklist.</li><li>Color contrast that meets WCAG AA for text and controls.</li><li>Labeled form fields with plain-language instructions.</li><li>Pages that resize and reflow on phones and when zoomed.</li><li>Respect for the “reduce motion” setting on your device.</li><li>Automated testing of every page with axe-core accessibility checks, most recently on {audit_date}.</li></ul>"),
            ("Video and audio", "<p>Job videos are hosted on YouTube. We are adding <b>captions</b> to our videos and written descriptions on each job page, so the key information is available without sound or sight. If a video you need is missing captions, tell us and we will provide the information in another format.</p>"),
            ("Known limitations", "<ul class=\"checks\"><li>Some third-party content, such as embedded YouTube players and maps, is controlled by those providers.</li><li>Some older videos may not yet have captions.</li><li>Downloadable documents are being reviewed; ask us for an accessible version of any document.</li></ul>"),
            ("Need help or found a problem?", "<p>If you have trouble using any part of this website, or need information in a different format, contact us and we will help:</p><p>Phone: {phone}<br>Email: {email}</p><p>We aim to respond within [[2 business days]]. If you are a government agency or procurement office reviewing our materials, we can provide accessible versions of our capability statement and other documents on request.</p>"),
            ("Ongoing review", "<p>We review the site for accessibility as we add new pages and videos. This statement was last reviewed on {audit_date}.</p>"),
        ],
    },
    {
        "slug": "compliance",
        "title": "Compliance & Certifications",
        "lead": "The policies and programs government agencies, prime contractors and owners look for — in one place.",
        "sections": [
            ("Drug-Free Workplace", "<p>{name} maintains a <b>Drug-Free Workplace program</b>. The unlawful manufacture, distribution, possession or use of controlled substances is prohibited in our workplace and on job sites. Our program includes a written policy provided to all employees, employee awareness, [[drug and alcohol testing — pre-employment / random / post-incident / reasonable suspicion — confirm]], and reporting requirements consistent with the federal Drug-Free Workplace Act of 1988 and Florida's drug-free workplace provisions (Section 287.087, Florida Statutes).</p>"),
            ("E-Verify", "<p>{name} is <b>registered with and uses E-Verify</b>, the federal employment eligibility verification system, to confirm the work authorization of all newly hired employees, as required for contractors working with Florida public agencies under Section 448.095, Florida Statutes. We require our subcontractors on public projects to provide affidavits that they do not employ, contract with or subcontract with unauthorized workers. E-Verify Company ID: [[XXX]].</p>"),
            ("Equal Opportunity & Non-Discrimination", "<p>{name} is an <b>equal opportunity employer</b>. We do not discriminate in employment, subcontracting or service on the basis of race, color, religion, sex, pregnancy, sexual orientation, gender identity, national origin, age, disability, genetic information, veteran status or any other characteristic protected by law. We comply with Title VII of the Civil Rights Act, the Americans with Disabilities Act, the Age Discrimination in Employment Act and applicable state and local laws, and with the equal opportunity clauses included in our public contracts.</p>"),
            ("Safety", "<p>Safety comes first on every job. Our safety program includes:</p><ul class=\"checks\"><li>Written safety program and site-specific safety planning.</li><li>OSHA-compliant practices and training: [[OSHA 10 / OSHA 30 / HAZWOPER — confirm]].</li><li>Daily job briefings and equipment inspections.</li><li>Experience Modification Rate (EMR): [[X.XX]] · Safety record: [[XXX]].</li></ul>"),
            ("Ethics & Integrity", "<ul class=\"checks\"><li>We do not offer or accept kickbacks, bribes or improper gifts, consistent with the federal Anti-Kickback Act and state procurement ethics laws.</li><li>We disclose potential conflicts of interest.</li><li>We bid honestly and do not collude with other bidders.</li></ul>"),
            ("Public Records", "<p>On contracts with Florida public agencies, we comply with the Florida Public Records Law (Chapter 119, Florida Statutes) as required by contract, including keeping and providing public records related to the work.</p>"),
            ("Licenses, Insurance & Registrations", "<p>Contractor licenses, insurance, bonding, SAM.gov registration (UEI / CAGE), NAICS codes, FEMA vendor and Army Corps information are listed on our <a href=\"{credentials}\">Licenses &amp; Credentials</a> page and in our <a href=\"{capability}\">Capability Statement</a>.</p>"),
            ("Documents available on request", "<ul class=\"checks\"><li>W-9</li><li>Certificate of Insurance (COI)</li><li>Drug-Free Workplace certification</li><li>E-Verify affidavit / MOU</li><li>Safety program summary and EMR letter</li><li>References and past performance</li></ul><p>Request documents: {email} · {phone}</p>"),
        ],
    },
    {
        "slug": "text-terms",
        "title": "Text Messaging Terms",
        "lead": "How our text messages work and how to stop them.",
        "sections": [
            ("Program", "<p>{name} sends text messages about bid requests, scheduling, project updates and service follow-ups to people who give us their mobile number and agree to receive texts.</p>"),
            ("Consent", "<p>By checking the text-message box on our forms, or by texting us first, you agree to receive text messages from {name} at the number you provide. <b>Consent is not a condition of any purchase or service.</b></p>"),
            ("Message frequency and cost", "<p>Message frequency varies based on your request or project. <b>Message and data rates may apply.</b></p>"),
            ("How to stop or get help", "<p>Reply <b>STOP</b> to any message to opt out. You will receive one confirmation and no further texts unless you opt in again. Reply <b>HELP</b> for help, or contact us at {phone} or {email}.</p>"),
            ("Carriers", "<p>Wireless carriers are not liable for delayed or undelivered messages.</p>"),
            ("Privacy", "<p>Mobile numbers and text messaging consent are not shared with or sold to third parties for marketing. See our <a href=\"{privacy}\">Privacy Policy</a>.</p>"),
        ],
    },
]

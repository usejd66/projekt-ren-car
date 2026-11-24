"""Përkthimet shqip (burimi). Pas ndryshimit:
    python locale/sq_translations.py && python manage.py compilemessages -l sq
Tekstet e reja: python manage.py makemessages -l sq, pastaj shtoji këtu.
"""
SQ = {
    # --- emailet / subjektet ---
    "We received your reservation #%(n)s – %(car)s": "E morëm rezervimin tuaj #%(n)s – %(car)s",
    "New reservation #%(n)s: %(car)s, %(start)s – %(end)s": "Rezervim i ri #%(n)s: %(car)s, %(start)s – %(end)s",
    "Your booking #%(n)s is confirmed – %(car)s": "Rezervimi juaj #%(n)s u konfirmua – %(car)s",
    "Your booking #%(n)s was cancelled": "Rezervimi juaj #%(n)s u anulua",
    "Contact form: %(subject)s": "Formulari i kontaktit: %(subject)s",
    "Cancellation request: reservation #%(n)s – %(car)s": "Kërkesë anulimi: rezervimi #%(n)s – %(car)s",
    "Cancelled by customer: reservation #%(n)s – %(car)s": "Anuluar nga klienti: rezervimi #%(n)s – %(car)s",
    "%(name)s – monthly report %(month)s: %(n)s bookings": "%(name)s – raporti mujor %(month)s: %(n)s rezervime",

    # --- formularët ---
    "Pickup location": "Vendi i marrjes",
    "Select a location": "Zgjidhni vendin",
    "Car": "Makina",
    "Full name": "Emri i plotë",
    "Email": "Email",
    "Phone": "Telefoni",
    "Pickup date": "Data e marrjes",
    "Return date": "Data e kthimit",
    "Notes": "Shënime",
    "First and last name": "Emri dhe mbiemri",
    "Please enter your first and last name.": "Ju lutem shkruani emrin dhe mbiemrin.",
    "Please enter a valid phone number.": "Ju lutem shkruani një numër telefoni të vlefshëm.",
    "The pickup date cannot be in the past.": "Data e marrjes nuk mund të jetë në të kaluarën.",
    "The return date must be after the pickup date.": "Data e kthimit duhet të jetë pas datës së marrjes.",
    "Name": "Emri",
    "Subject": "Subjekti",
    "Message": "Mesazhi",
    "An account with this email already exists.": "Ekziston tashmë një llogari me këtë email.",
    "This email is already subscribed.": "Ky email është abonuar tashmë.",

    # --- modelet ---
    "Economy": "Ekonomike",
    "SUV": "SUV",
    "Luxury": "Luksoze",
    "Family / Van": "Familjare / Van",
    "Manual": "Manuale",
    "Automatic": "Automatike",
    "Petrol": "Benzinë",
    "Diesel": "Naftë",
    "Hybrid": "Hibride",
    "Electric": "Elektrike",
    "A reservation cannot be longer than %(days)s days.": "Një rezervim nuk mund të jetë më i gjatë se %(days)s ditë.",
    "This car is already booked on the selected dates.": "Kjo makinë është e zënë në datat e zgjedhura.",

    # --- rezervimet e mia ---
    "Cancelled": "Anuluar",
    "Cancellation requested": "Kërkuar anulimi",
    "Completed": "Përfunduar",
    "Confirmed": "Konfirmuar",
    "Awaiting confirmation": "Në pritje të konfirmimit",
    "Reservation #%(n)s · booked %(date)s": "Rezervimi #%(n)s · bërë më %(date)s",
    "Pickup": "Marrja",
    "Return": "Kthimi",
    "Total": "Totali",
    "Cancel booking": "Anulo rezervimin",
    "Request cancellation": "Kërko anulimin",
    "Book again": "Rezervo sërish",

    # --- JavaScript ---
    "Select pickup date": "Zgjidhni datën e marrjes",
    "Select return date": "Zgjidhni datën e kthimit",
    "Then choose the return date": "Pastaj zgjidhni datën e kthimit",
    "Pickup: {date}": "Marrja: {date}",
    "day": "ditë",
    "days": "ditë",
    "/ day": "/ ditë",
    "{n} seats": "{n} ulëse",
    "No car selected": "Asnjë makinë e zgjedhur",
    "Daily rate": "Çmimi ditor",
    "Choose your dates": "Zgjidhni datat",
    "This car is booked from {start} to {end}. Please choose different dates.": "Kjo makinë është e zënë nga {start} deri më {end}. Ju lutem zgjidhni data të tjera.",
    "This car is booked on the selected dates.": "Kjo makinë është e zënë në datat e zgjedhura.",
    "Please select a car.": "Ju lutem zgjidhni një makinë.",
    "Please select a pickup location.": "Ju lutem zgjidhni vendin e marrjes.",
    "Please select your dates.": "Ju lutem zgjidhni datat.",
    "From": "Nga",
    "total": "gjithsej",
    "Continue": "Vazhdo",
    "Check dates": "Shiko datat",
    "Language": "Gjuha",

    # --- kërkimi ---
    "Add date": "Shto datën",
    "Find a car": "Gjej makinë",

    # --- About ---
    "About Us": "Rreth nesh",
    "%(name)s is a car rental company in %(city)s offering modern cars, clear prices and simple online booking, with pickup in %(locations)s.":
        "%(name)s është një kompani me makina me qira në %(city)s, me makina moderne, çmime të qarta dhe rezervim të thjeshtë online, me marrje në %(locations)s.",
    "About %(name)s": "Rreth %(name)s",
    "A local car rental company in %(city)s, built around one idea: renting a car should be simple.":
        "Një kompani vendase me makina me qira në %(city)s, e ndërtuar mbi një ide: marrja e një makine me qira duhet të jetë e thjeshtë.",
    "A %(name)s rental car": "Një makinë me qira e %(name)s",
    "Your trip, our cars": "Udhëtimi juaj, makinat tona",
    "Whether you are travelling for business, on holiday, or just need a reliable car for a few days, we want the rental to be the easy part of your trip.":
        "Qoftë për punë, për pushime apo thjesht ju duhet një makinë e sigurt për disa ditë, duam që qiraja të jetë pjesa më e lehtë e udhëtimit tuaj.",
    "That is why you see the total price before you book, you can reserve online in a couple of minutes, and a real team in %(city)s is there when you need help.":
        "Prandaj e shihni çmimin total para se të rezervoni, mund të rezervoni online për pak minuta dhe një ekip i vërtetë në %(city)s është aty kur ju duhet ndihmë.",
    "See our cars": "Shikoni makinat tona",
    "What we stand for": "Për çfarë qëndrojmë",
    "Three promises behind every rental.": "Tri premtime pas çdo qiraje.",
    "Well-kept cars": "Makina të mirëmbajtura",
    "Every car is cleaned and checked before each rental, so it is ready when you are.":
        "Çdo makinë pastrohet dhe kontrollohet para çdo qiraje, që të jetë gati kur jeni ju.",
    "Clear prices": "Çmime të qarta",
    "One daily price and a total you see before you confirm. No surprises at pickup.":
        "Një çmim ditor dhe një total që e shihni para se të konfirmoni. Pa surpriza në marrje.",
    "Real support": "Mbështetje e vërtetë",
    "Questions before or during your rental? Call or message our team in %(city)s.":
        "Keni pyetje para ose gjatë qirasë? Telefononi ose shkruani ekipit tonë në %(city)s.",
    "Where to pick up your car": "Ku ta merrni makinën",
    "Choose the location when you book.": "Zgjidhni vendin kur rezervoni.",
    "Pickup & return": "Marrja & kthimi",
    "Ready when you are": "Gati kur jeni ju",
    "Pick your dates and see which cars are available.": "Zgjidhni datat dhe shikoni cilat makina janë të lira.",
    "Contact us": "Na kontaktoni",
    "Browse cars": "Shiko makinat",

    # --- base ---
    "%(name)s – Car Rental in %(city)s": "%(name)s – Makina me qira në %(city)s",
    "Rent a car in %(city)s with %(name)s: modern cars, clear prices and easy online booking.":
        "Merrni makinë me qira në %(city)s me %(name)s: makina moderne, çmime të qarta dhe rezervim i lehtë online.",
    "Modern cars, clear prices and easy online booking in %(city)s.": "Makina moderne, çmime të qarta dhe rezervim i lehtë online në %(city)s.",
    "Open menu": "Hap menunë",
    "Close menu": "Mbyll menunë",
    "Home": "Kreu",
    "Cars": "Makinat",
    "Contact": "Kontakt",
    "Sign out": "Dil",
    "My bookings": "Rezervimet e mia",
    "Sign In": "Hyr",
    "Reserve Now": "Rezervo tani",
    "Car rental in %(city)s with modern cars, clear prices and simple online booking.":
        "Makina me qira në %(city)s, me makina moderne, çmime të qarta dhe rezervim të thjeshtë online.",
    "Get offers by email": "Merrni oferta me email",
    "Your email address": "Adresa juaj e email-it",
    "Subscribe": "Abonohu",
    "Footer": "Fundi i faqes",
    "Explore": "Eksploro",
    "Our cars": "Makinat tona",
    "Reserve a car": "Rezervo një makinë",
    "Rental terms": "Kushtet e qirasë",
    "About us": "Rreth nesh",
    "Pickup locations": "Vendet e marrjes",
    "All rights reserved.": "Të gjitha të drejtat e rezervuara.",
    "Hi %(name)s, I'd like to rent a car.": "Përshëndetje %(name)s, dua të marr një makinë me qira.",
    "Chat with us on WhatsApp": "Na shkruani në WhatsApp",
    "Chat with us": "Na shkruani",

    # --- faqja e makinës ---
    "%(car)s – rent from €%(price)s/day | %(name)s": "%(car)s – me qira nga €%(price)s/ditë | %(name)s",
    "Rent the %(car)s in %(city)s from €%(price)s per day. %(gear)s, %(fuel)s, %(seats)s seats. Check availability and book online.":
        "Merrni me qira %(car)s në %(city)s nga €%(price)s në ditë. %(gear)s, %(fuel)s, %(seats)s ulëse. Shikoni disponueshmërinë dhe rezervoni online.",
    "%(car)s – %(name)s car rental": "%(car)s – makina me qira %(name)s",
    "From €%(price)s per day · %(gear)s · %(seats)s seats": "Nga €%(price)s në ditë · %(gear)s · %(seats)s ulëse",
    "Breadcrumb": "Navigimi",
    "Photos of the %(car)s": "Fotot e %(car)s",
    "Previous photo": "Foto e mëparshme",
    "Next photo": "Foto tjetër",
    "Choose photo": "Zgjidhni foton",
    "Photo": "Foto",
    "Seats": "Ulëse",
    "Transmission": "Kambio",
    "Fuel": "Karburanti",
    "Year": "Viti",
    "About this car": "Rreth kësaj makine",
    "Included in the price": "Të përfshira në çmim",
    "Unlimited kilometres": "Kilometra pa limit",
    "Pickup in %(locations)s": "Marrje në %(locations)s",
    "Cleaned and checked before every rental": "E pastruar dhe e kontrolluar para çdo qiraje",
    "Local support during your rental": "Mbështetje vendase gjatë qirasë",
    "Details": "Detajet",
    "Book the %(car)s": "Rezervo %(car)s",
    "Continue to booking": "Vazhdo me rezervimin",
    "No payment taken online": "Pa pagesë online",
    "Booked dates are crossed out": "Datat e zëna janë të vizatuara",
    "Currently unavailable": "Aktualisht e padisponueshme",
    "This car can't be booked right now. Have a look at similar cars below or contact us.":
        "Kjo makinë nuk mund të rezervohet tani. Shikoni makinat e ngjashme më poshtë ose na kontaktoni.",
    "Browse available cars": "Shiko makinat e lira",
    "Similar cars": "Makina të ngjashme",
    "See all %(cat)s": "Shiko të gjitha: %(cat)s",
    "Book now": "Rezervo",

    # --- Cars ---
    "Available Cars": "Makinat e lira",
    "Our Cars": "Makinat tona",
    "Browse the %(name)s fleet in %(city)s: filter by category, transmission and price, check availability for your dates and book online.":
        "Shikoni flotën e %(name)s në %(city)s: filtroni sipas kategorisë, kambios dhe çmimit, shikoni disponueshmërinë për datat tuaja dhe rezervoni online.",
    "Available cars": "Makinat e lira",
    "Update": "Përditëso",
    "Pickup: %(loc)s": "Marrja: %(loc)s",
    "Clear dates": "Hiq datat",
    "Categories": "Kategoritë",
    "All": "Të gjitha",
    "Filters": "Filtrat",
    "Close": "Mbyll",
    "Search": "Kërko",
    "Brand or model": "Marka ose modeli",
    "Any": "Çdo",
    "Max price / day": "Çmimi maks. / ditë",
    "Sort by": "Rendit sipas",
    "Newest": "Më të rejat",
    "Price: low to high": "Çmimi: nga më i ulëti",
    "Price: high to low": "Çmimi: nga më i larti",
    "Apply": "Apliko",
    "Reset": "Pastro",
    "No cars available for these dates": "Nuk ka makina të lira për këto data",
    "No cars match your search": "Asnjë makinë nuk përputhet me kërkimin",
    "Try different dates or remove some filters.": "Provoni data të tjera ose hiqni disa filtra.",
    "Try removing some filters.": "Provoni të hiqni disa filtra.",
    "Show all cars": "Shiko të gjitha makinat",
    "Pages": "Faqet",
    "Previous": "Para",
    "Page %(n)s of %(total)s": "Faqja %(n)s nga %(total)s",
    "Next": "Pas",

    # --- Contact ---
    "Contact %(name)s in %(city)s for help choosing a car, making a reservation or any question about renting a car.":
        "Kontaktoni %(name)s në %(city)s për ndihmë me zgjedhjen e makinës, rezervimin ose çdo pyetje për qiranë.",
    "Need help choosing a car or have a question about a booking? We usually reply within a few hours.":
        "Ju duhet ndihmë me zgjedhjen e makinës apo keni një pyetje për një rezervim? Zakonisht përgjigjemi brenda pak orësh.",
    "Call us": "Na telefononi",
    "Message us any time": "Na shkruani në çdo kohë",
    "Opening hours": "Orari",
    "Send us a message": "Na dërgoni një mesazh",
    "Send message": "Dërgo mesazhin",
    "%(name)s location on the map": "Vendndodhja e %(name)s në hartë",

    # --- emailet (përmbajtja) ---
    "Reservation": "Rezervimi",
    "Cancellation request #%(n)s": "Kërkesë anulimi #%(n)s",
    "Booking #%(n)s cancelled by the customer": "Rezervimi #%(n)s u anulua nga klienti",
    "%(name)s asked to cancel this <strong>confirmed</strong> booking. Please decide in the admin and let the customer know.":
        "%(name)s kërkoi anulimin e këtij rezervimi të <strong>konfirmuar</strong>. Vendosni te admin-i dhe njoftoni klientin.",
    "%(name)s cancelled this booking before it was confirmed. The dates are free again.":
        "%(name)s e anuloi këtë rezervim para se të konfirmohej. Datat janë sërish të lira.",
    "Customer": "Klienti",
    "Open in admin": "Hape te admin-i",
    "Your booking was cancelled": "Rezervimi juaj u anulua",
    "Hi %(name)s, your reservation #%(n)s for the %(car)s (%(start)s – %(end)s) has been cancelled.":
        "Përshëndetje %(name)s, rezervimi juaj #%(n)s për %(car)s (%(start)s – %(end)s) u anulua.",
    "If this is unexpected or you'd like to book different dates, reply to this email or call":
        "Nëse kjo është e papritur ose dëshironi të rezervoni data të tjera, përgjigjuni këtij email-i ose telefononi",
    "See available cars": "Shiko makinat e lira",
    "Hi %(name)s,": "Përshëndetje %(name)s,",
    "Your reservation #%(n)s for the %(car)s (%(start)s – %(end)s) has been cancelled.":
        "Rezervimi juaj #%(n)s për %(car)s (%(start)s – %(end)s) u anulua.",
    "Your booking is confirmed": "Rezervimi juaj u konfirmua",
    "Hi %(name)s, good news: your %(car)s will be ready for you.": "Përshëndetje %(name)s, lajm i mirë: %(car)s do të jetë gati për ju.",
    "At pickup, please bring:": "Në marrje, ju lutem sillni:",
    "A valid driving licence and an ID card or passport.": "Patentën e vlefshme dhe kartën e identitetit ose pasaportën.",
    "Need to change something? Reply to this email or call": "Doni të ndryshoni diçka? Përgjigjuni këtij email-i ose telefononi",
    "Good news: your booking is confirmed and your %(car)s will be ready for you.":
        "Lajm i mirë: rezervimi juaj u konfirmua dhe %(car)s do të jetë gati për ju.",
    "At pickup, please bring a valid driving licence and an ID card or passport.":
        "Në marrje, ju lutem sillni patentën e vlefshme dhe kartën e identitetit ose pasaportën.",
    "Need to change something? Reply to this email or call %(phone)s.": "Doni të ndryshoni diçka? Përgjigjuni këtij email-i ose telefononi %(phone)s.",
    "New reservation #%(n)s": "Rezervim i ri #%(n)s",
    "A new booking is waiting for your confirmation.": "Një rezervim i ri pret konfirmimin tuaj.",
    "We received your reservation": "E morëm rezervimin tuaj",
    "Hi %(name)s, thank you for choosing %(site_name)s. We'll check availability and contact you shortly to confirm your booking.":
        "Përshëndetje %(name)s, faleminderit që zgjodhët %(site_name)s. Do të kontrollojmë disponueshmërinë dhe do t'ju kontaktojmë së shpejti për të konfirmuar rezervimin.",
    "What happens next?": "Çfarë ndodh më pas?",
    "You'll get another email as soon as your booking is confirmed. No payment is taken online.":
        "Do të merrni një email tjetër sapo rezervimi të konfirmohet. Nuk merret asnjë pagesë online.",
    "Questions? Just reply to this email or call us on": "Keni pyetje? Thjesht përgjigjuni këtij email-i ose na telefononi në",
    "Thank you for choosing %(site_name)s. We received your reservation and will contact you shortly to confirm it.":
        "Faleminderit që zgjodhët %(site_name)s. E morëm rezervimin tuaj dhe do t'ju kontaktojmë së shpejti për ta konfirmuar.",
    "Questions? Reply to this email or call %(phone)s.": "Keni pyetje? Përgjigjuni këtij email-i ose telefononi %(phone)s.",
    "New message from the website": "Mesazh i ri nga faqja",
    "Reply to this email to answer %(name)s directly.": "Përgjigjuni këtij email-i për t'i shkruar direkt %(name)s.",
    "Your website in %(month)s": "Faqja juaj në %(month)s",
    "How many customers the %(name)s website brought this month.": "Sa klientë solli faqja e %(name)s këtë muaj.",
    "Bookings": "Rezervime",
    "%(n)s the month before": "%(n)s muajin e kaluar",
    "Booking value": "Vlera e rezervimeve",
    "€%(n)s the month before": "€%(n)s muajin e kaluar",
    "WhatsApp clicks": "Klikime WhatsApp",
    "Phone clicks": "Klikime telefon",
    "Contact messages": "Mesazhe nga Contact",
    "Email clicks": "Klikime email",
    "Where customers came from": "Nga erdhën klientët",
    "%(b)s bookings · %(c)s contacts": "%(b)s rezervime · %(c)s kontakte",
    "Most booked cars": "Makinat më të rezervuara",
    "See all results": "Shiko të gjitha rezultatet",

    # --- faqja kryesore ---
    "Car Rental in %(city)s | %(name)s": "Makina me qira në %(city)s | %(name)s",
    "Rent a car in %(city)s with %(name)s: modern cars, clear prices and easy online booking. Pickup in %(locations)s.":
        "Merrni makinë me qira në %(city)s me %(name)s: makina moderne, çmime të qarta dhe rezervim i lehtë online. Marrje në %(locations)s.",
    "Car rental in %(city)s,<br>made simple.": "Qira makinash në %(city)s,<br>e thjeshtë.",
    "Modern, well-maintained cars with clear prices. Pick up in %(locations)s.":
        "Makina moderne dhe të mirëmbajtura, me çmime të qarta. Marrje në %(locations)s.",
    "From <strong>€%(price)s</strong> per day": "Nga <strong>€%(price)s</strong> në ditë",
    "Total price shown before you book": "Çmimi total para se të rezervoni",
    "Book online in under 2 minutes": "Rezervoni online për më pak se 2 minuta",
    "Choose your car": "Zgjidhni makinën",
    "From city cars to family vans, all with unlimited kilometres.": "Nga makinat e qytetit te furgonët familjarë, të gjitha me kilometra pa limit.",
    "View all cars": "Shiko të gjitha makinat",
    "How it works": "Si funksionon",
    "Three steps, no paperwork at the counter.": "Tre hapa, pa letra në sportel.",
    "Step": "Hapi",
    "Choose a car": "Zgjidhni makinën",
    "Browse the fleet and compare prices, seats and transmission.": "Shikoni flotën dhe krahasoni çmimet, ulëset dhe kambion.",
    "Pick dates & location": "Zgjidhni datat & vendin",
    "Select pickup and return dates. You see the total price right away.": "Zgjidhni datat e marrjes dhe kthimit. Çmimin total e shihni menjëherë.",
    "Collect your keys": "Merrni çelësat",
    "We confirm your booking and have the car ready when you arrive.": "Ne e konfirmojmë rezervimin dhe makina është gati kur të vini.",
    "Rental terms at a glance": "Kushtet e qirasë shkurt",
    "No surprises at pickup. Here is what's included and what we need from you.": "Pa surpriza në marrje. Ja çfarë përfshihet dhe çfarë na duhet nga ju.",
    "Full rental terms": "Të gjitha kushtet",
    "Why rent with %(name)s": "Pse të zgjidhni %(name)s",
    "Well-maintained cars": "Makina të mirëmbajtura",
    "Every car is cleaned and checked before each rental.": "Çdo makinë pastrohet dhe kontrollohet para çdo qiraje.",
    "Clear pricing": "Çmime të qarta",
    "One daily price. The total is calculated before you confirm.": "Një çmim ditor. Totali llogaritet para se të konfirmoni.",
    "Flexible pickup": "Marrje fleksibile",
    "Collect your car in %(locations)s.": "Merreni makinën në %(locations)s.",
    "Local support": "Mbështetje vendase",
    "A real team in %(city)s you can call or message during your rental.": "Një ekip i vërtetë në %(city)s që mund ta telefononi ose t'i shkruani gjatë qirasë.",
    "What customers say": "Çfarë thonë klientët",
    "%(r)s out of 5": "%(r)s nga 5",
    "Questions & answers": "Pyetje & përgjigje",
    "Can't find what you're looking for?": "Nuk e gjeni atë që kërkoni?",
    "What documents do I need to rent a car?": "Çfarë dokumentesh më duhen për të marrë një makinë me qira?",
    "A valid driving licence and an identity document (ID card or passport). Additional requirements may apply depending on the vehicle.":
        "Patentë e vlefshme dhe një dokument identifikimi (kartë identiteti ose pasaportë). Për disa makina mund të ketë kërkesa shtesë.",
    "How do I book a car?": "Si rezervoj një makinë?",
    "Choose a car on the Cars page or use the search above, select your dates and pickup location, and submit the reservation. We confirm it by email or phone.":
        "Zgjidhni një makinë te faqja Makinat ose përdorni kërkimin më sipër, zgjidhni datat dhe vendin e marrjes dhe dërgoni rezervimin. Ne e konfirmojmë me email ose telefon.",
    "Can I choose a specific car?": "A mund të zgjedh një makinë të caktuar?",
    "Yes. You book the exact model you select. The calendar shows which dates are already taken.":
        "Po. Rezervoni pikërisht modelin që zgjidhni. Kalendari tregon cilat data janë të zëna.",
    "Can I cancel my reservation?": "A mund ta anuloj rezervimin?",
    'See all <a href="%(url)s">rental terms</a>.': 'Shikoni të gjitha <a href="%(url)s">kushtet e qirasë</a>.',
    "How can I contact %(name)s?": "Si mund ta kontaktoj %(name)s?",
    "Call us on %(phone)s, email %(email)s, or use the form on the Contact page.":
        "Na telefononi në %(phone)s, na shkruani në %(email)s ose përdorni formularin te faqja Kontakt.",
    "Not sure which car to pick?": "Nuk jeni i sigurt cilën makinë të zgjidhni?",
    "Call us and we'll help you choose the right car for your trip.": "Na telefononi dhe ju ndihmojmë të zgjidhni makinën e duhur për udhëtimin tuaj.",

    # --- faqet e vendeve ---
    "Car Rental at %(loc)s | %(name)s": "Makina me qira – %(loc)s | %(name)s",
    "Car Rental in %(loc)s | %(name)s": "Makina me qira – %(loc)s | %(name)s",
    "Rent a car in %(loc)s with %(name)s. Clear prices, unlimited kilometres and easy online booking.":
        "Makina me qira – %(loc)s, me %(name)s. Çmime të qarta, kilometra pa limit dhe rezervim i lehtë online.",
    "Car rental at %(loc)s": "Makina me qira – %(loc)s",
    "Car rental in %(loc)s": "Makina me qira – %(loc)s",
    "Pick up your car right when you land and start your trip without queues or taxis.":
        "Merreni makinën sapo të zbrisni nga avioni dhe nisni udhëtimin pa radhë dhe pa taksi.",
    "Collect your car in %(loc)s at a time that suits you and drive wherever you want.":
        "Merreni makinën – %(loc)s – në orën që ju përshtatet dhe udhëtoni ku të doni.",
    "Prices from <strong>€%(price)s per day</strong>.": "Çmime nga <strong>€%(price)s në ditë</strong>.",
    "Cars available in %(loc)s": "Makinat e lira – %(loc)s",
    "Choose your dates above to see the total price.": "Zgjidhni datat më sipër për të parë çmimin total.",
    "All cars": "Të gjitha makinat",
    "Other pickup locations": "Vende të tjera marrjeje",

    # --- login / signup ---
    "Sign in to your %(name)s account to manage your car rental reservations.":
        "Hyni në llogarinë tuaj %(name)s për të menaxhuar rezervimet.",
    "Welcome back": "Mirë se u kthyet",
    "Sign in to your %(name)s account.": "Hyni në llogarinë tuaj %(name)s.",
    "The username or password is incorrect. Please try again.": "Emri i përdoruesit ose fjalëkalimi është i gabuar. Provoni sërish.",
    "Username": "Emri i përdoruesit",
    "Password": "Fjalëkalimi",
    "Show or hide password": "Shfaq ose fshih fjalëkalimin",
    "Sign in": "Hyr",
    "New to %(name)s?": "I ri te %(name)s?",
    "Create an account": "Krijoni një llogari",
    "Create Account": "Krijo llogari",
    "Create your %(name)s account to reserve your next rental car faster.":
        "Krijoni llogarinë tuaj %(name)s për të rezervuar më shpejt herën tjetër.",
    "Create your account": "Krijoni llogarinë tuaj",
    "Book faster next time, with your details already filled in.": "Rezervoni më shpejt herën tjetër, me të dhënat tuaja të plotësuara.",
    "At least 8 characters, not only numbers.": "Të paktën 8 karaktere, jo vetëm numra.",
    "Confirm password": "Konfirmoni fjalëkalimin",
    "Create account": "Krijo llogarinë",
    "Already have an account?": "Keni tashmë llogari?",

    # --- My bookings ---
    "Hi %(name)s. Here you can see your reservations and cancel upcoming ones.":
        "Përshëndetje %(name)s. Këtu shihni rezervimet tuaja dhe mund të anuloni ato që vijnë.",
    "No bookings yet": "Ende asnjë rezervim",
    "When you reserve a car while signed in, it will show up here.": "Kur rezervoni një makinë ndërsa jeni i kyçur, ajo do të shfaqet këtu.",
    "Upcoming": "Të ardhshme",
    "Past & cancelled": "Të kaluara & të anuluara",
    'Need to change dates or have a question? <a href="%(url)s">Contact us</a> or call <a href="tel:%(tel)s">%(phone)s</a>.':
        'Doni të ndryshoni datat apo keni një pyetje? <a href="%(url)s">Na kontaktoni</a> ose telefononi <a href="tel:%(tel)s">%(phone)s</a>.',
    "Keep booking": "Mbaje rezervimin",
    "Cancel this booking?": "Ta anuloni këtë rezervim?",
    "Request cancellation?": "Të kërkoni anulimin?",
    "Your booking hasn't been confirmed yet, so it will be cancelled right away and the dates released.":
        "Rezervimi juaj nuk është konfirmuar ende, ndaj do të anulohet menjëherë dhe datat do të lirohen.",
    "Your booking is already confirmed. We'll receive your request and contact you to arrange the cancellation.":
        "Rezervimi juaj është i konfirmuar. Do ta marrim kërkesën dhe do t'ju kontaktojmë për anulimin.",
    "Yes, cancel booking": "Po, anuloje",
    "Send request": "Dërgo kërkesën",

    # --- offline / kushtet ---
    "You're offline": "Jeni pa internet",
    "Check your internet connection and try again. You can still call or message us.":
        "Kontrolloni lidhjen me internetin dhe provoni sërish. Mund të na telefononi ose të na shkruani.",
    "Try again": "Provo sërish",
    "%(name)s rental terms: driver requirements, deposit, insurance, fuel policy, mileage and cancellation.":
        "Kushtet e qirasë së %(name)s: kërkesat për shoferin, depozita, sigurimi, karburanti, kilometrat dhe anulimi.",
    "Everything you need to know before you book. Clear and simple, no small print.":
        "Gjithçka që duhet të dini para se të rezervoni. E qartë dhe e thjeshtë, pa shkrime të vogla.",
    "Still have a question about the terms?": "Keni ende pyetje për kushtet?",

    # --- rezervimi ---
    "Reserve a Car": "Rezervo një makinë",
    "Reserve your %(name)s rental car online: choose your car, dates and pickup location and see the total price before you confirm.":
        "Rezervoni online makinën me qira te %(name)s: zgjidhni makinën, datat dhe vendin e marrjes dhe shikoni çmimin total para se të konfirmoni.",
    "Back to cars": "Kthehu te makinat",
    "Complete your reservation": "Përfundoni rezervimin",
    "It takes about 2 minutes. No payment is taken online.": "Zgjat rreth 2 minuta. Nuk merret asnjë pagesë online.",
    "Please check the highlighted fields.": "Ju lutem kontrolloni fushat e theksuara.",
    "Your car": "Makina juaj",
    "Select a car…": "Zgjidhni një makinë…",
    "Select date": "Zgjidhni datën",
    "Dates that are already booked for this car are crossed out in the calendar.":
        "Datat që janë tashmë të zëna për këtë makinë janë të vizatuara në kalendar.",
    "Driver details": "Të dhënat e shoferit",
    "optional": "opsionale",
    "Booking summary": "Përmbledhja e rezervimit",
    "Confirm reservation": "Konfirmo rezervimin",
    "Total price shown, no hidden fees": "Çmimi total i dukshëm, pa tarifa të fshehura",
    "We contact you to confirm the booking": "Ju kontaktojmë për të konfirmuar rezervimin",
    'By confirming you accept our <a href="%(url)s" target="_blank" rel="noopener">rental terms</a>.':
        'Duke konfirmuar pranoni <a href="%(url)s" target="_blank" rel="noopener">kushtet e qirasë</a>.',
    "Confirm": "Konfirmo",
    "Reservation received": "Rezervimi u mor",
    "Thank you, %(name)s. We'll contact you at <strong>%(email)s</strong> or <strong>%(phone)s</strong> to confirm your booking.":
        "Faleminderit, %(name)s. Do t'ju kontaktojmë në <strong>%(email)s</strong> ose <strong>%(phone)s</strong> për të konfirmuar rezervimin.",
    "Reservation #%(n)s": "Rezervimi #%(n)s",
    "Back to home": "Kthehu në kreu",
    "View my bookings": "Shiko rezervimet e mia",
    "Browse more cars": "Shiko makina të tjera",

    # --- mesazhet nga views.py ---
    "Please choose both a pickup and a return date.": "Ju lutem zgjidhni datën e marrjes dhe të kthimit.",
    "A rental cannot be longer than %(days)s days.": "Qiraja nuk mund të jetë më e gjatë se %(days)s ditë.",
    "Thank you! Your message has been sent. We'll get back to you shortly.": "Faleminderit! Mesazhi u dërgua. Do t'ju përgjigjemi së shpejti.",
    "This car was just booked for the selected dates. Please choose different dates.":
        "Kjo makinë sapo u rezervua për datat e zgjedhura. Ju lutem zgjidhni data të tjera.",
    "This booking can no longer be cancelled online. Please contact us.": "Ky rezervim nuk mund të anulohet më online. Ju lutem na kontaktoni.",
    "Booking #%(n)s has been cancelled.": "Rezervimi #%(n)s u anulua.",
    "Your cancellation request was sent. We'll contact you shortly.": "Kërkesa për anulim u dërgua. Do t'ju kontaktojmë së shpejti.",
    "Your account has been created. Welcome to %(name)s!": "Llogaria juaj u krijua. Mirë se vini te %(name)s!",
    "Thank you! You are now subscribed to our newsletter.": "Faleminderit! Tani jeni abonuar në buletinin tonë.",
}

# Format shumës (njëjës, shumës)
SQ_PLURAL = {
    "%(n)s day": ("%(n)s ditë", "%(n)s ditë"),
    "%(n)s car available for your dates": ("%(n)s makinë e lirë për datat tuaja", "%(n)s makina të lira për datat tuaja"),
    "%(n)s car found": ("U gjet %(n)s makinë", "U gjetën %(n)s makina"),
    "%(n)s seat": ("%(n)s ulëse", "%(n)s ulëse"),
    "<strong>€%(total)s</strong> total · %(n)s day": ("<strong>€%(total)s</strong> gjithsej · %(n)s ditë", "<strong>€%(total)s</strong> gjithsej · %(n)s ditë"),
    "Pickup in %(n)s location": ("Marrje në %(n)s vend", "Marrje në %(n)s vende"),
    "%(n)s car": ("%(n)s makinë", "%(n)s makina"),
    '<strong class="text-dark">%(avg)s</strong> out of 5 · %(n)s review':
        ('<strong class="text-dark">%(avg)s</strong> nga 5 · %(n)s vlerësim', '<strong class="text-dark">%(avg)s</strong> nga 5 · %(n)s vlerësime'),
}


if __name__ == "__main__":
    import pathlib
    import re

    import polib

    path = pathlib.Path(__file__).parent / "sq" / "LC_MESSAGES" / "django.po"
    po = polib.pofile(str(path))
    po.metadata["Plural-Forms"] = "nplurals=2; plural=(n != 1);"
    po.metadata["Language"] = "sq"
    missing, bad = [], []
    for entry in po:
        if entry.obsolete:
            continue
        if entry.msgid_plural:
            pair = SQ_PLURAL.get(entry.msgid)
            if not pair:
                missing.append(entry.msgid)
                continue
            entry.msgstr_plural = {0: pair[0], 1: pair[1]}
            texts = pair
        else:
            text = SQ.get(entry.msgid)
            if text is None:
                missing.append(entry.msgid)
                continue
            entry.msgstr = text
            texts = (text,)
        # vende-mbajtëset duhet të jenë të njëjta në përkthim
        holders = set(re.findall(r"%\(\w+\)s|\{\w+\}", entry.msgid))
        for t in texts:
            if set(re.findall(r"%\(\w+\)s|\{\w+\}", t)) - holders or (holders - set(re.findall(r"%\(\w+\)s|\{\w+\}", t)) and not entry.msgid_plural):
                bad.append(entry.msgid)
        if "fuzzy" in entry.flags:
            entry.flags.remove("fuzzy")
    po.save()
    print(f"translated: {len(po.translated_entries())}/{len([e for e in po if not e.obsolete])}")
    if missing:
        print("MISSING:", *missing, sep="\n  ")
    if bad:
        print("PLACEHOLDER MISMATCH:", *bad, sep="\n  ")

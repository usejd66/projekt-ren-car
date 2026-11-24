# DriveOn - Car Rental Website

Website për qiradhënien e makinave, i ndërtuar me **Django** (backend) dhe **HTML, CSS, JavaScript dhe Bootstrap** (frontend).

## Funksionalitetet

- Faqet: Home, Cars, Explore Fleet, About Us, Contact Us, Reservation
- Makinat, rishikimet (reviews) dhe rezervimet merren dinamikisht nga databaza
- Kërkim dhe filtrim i makinave (emër/brand, kategori, transmision, çmim, renditje) me faqosje
- Rezervim makine me kontroll për mbivendosje datash dhe llogaritje automatike të çmimit total
- Forma Contact Us: mesazhet ruhen në databazë dhe shfaqet mesazh konfirmimi
- Regjistrim (Sign Up), hyrje (Log In) dhe dalje (Log Out)
- Abonim në newsletter (Subscribe)
- Panel admin për menaxhimin e makinave, rezervimeve, rishikimeve, mesazheve dhe abonentëve
- Dizajn responsive (i përshtatshëm për telefon)

## Teknologjitë

- Python 3 dhe Django
- SQLite (databaza)
- Pillow (për ngarkimin e imazheve të makinave)
- HTML, CSS, JavaScript, Bootstrap 5, Font Awesome

## Instalimi dhe ekzekutimi

1. Klono projektin dhe hyr në folder:

   ```bash
   git clone <linku-i-repository>
   cd projekt-ren-car
   ```

2. (Opsionale) Krijo dhe aktivizo një virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. Instalo varësitë:

   ```bash
   pip install django pillow
   ```

   Nëse projekti ka skedarin `requirements.txt`, përdor:

   ```bash
   pip install -r requirements.txt
   ```

4. Krijo tabelat e databazës:

   ```bash
   python manage.py migrate
   ```

5. Krijo një llogari administratori:

   ```bash
   python manage.py createsuperuser
   ```

6. Nise serverin:

   ```bash
   python manage.py runserver
   ```

7. Hape shfletuesin te: **http://127.0.0.1:8000/**

## Shtimi i makinave

1. Hyr te **http://127.0.0.1:8000/admin/** me llogarinë e administratorit.
2. Shko te **Cars** dhe shto makina (me foto, çmim dhe kategori).
3. Shëno **"Is featured"** për makinat që duhet të shfaqen edhe në faqen kryesore.

Rishikimet (**Reviews**) shfaqen në website vetëm pasi t'i miratosh nga admin (**Is approved**).

## Ribrandimi për një klient të ri

Gjithë marka është në **një skedar**: [`car_app/branding.py`](car_app/branding.py).

1. Ndrysho emrin, logon (si tekst ose imazh), ngjyrën, qytetin, vendet e marrjes dhe kontaktet.
2. Zëvendëso foton e hero-s: `car_app/static/image/hero1.webp` (desktop) dhe `hero1-mobile.webp` (telefon).
3. (opsionale) Favicon: `car_app/static/image/favicon-32.png`, `apple-touch-icon.png`, `icon-512.png`.
4. Në produksion: `python manage.py collectstatic`.

Emri, ngjyra dhe kontaktet përditësohen automatikisht në të gjitha faqet, në email-e,
te butoni WhatsApp, te manifesti i aplikacionit (PWA) dhe te të dhënat për Google.

## Emailet

Faqja dërgon automatikisht:

- **klientit**: konfirmimin që rezervimi u mor, dhe një email tjetër kur e konfirmon ose e anulon te admin;
- **ty** (`BOOKINGS_EMAIL`): njoftim për çdo rezervim të ri (me lidhje te admin) dhe çdo mesazh nga Contact.

Në zhvillim emailet shfaqen në terminal. Në produksion vendos këto variabla mjedisi:

| Variabla | Shembull |
|---|---|
| `EMAIL_HOST` | `smtp.gmail.com` (ose `smtp-relay.brevo.com`) |
| `EMAIL_PORT` | `587` |
| `EMAIL_HOST_USER` | adresa / përdoruesi SMTP |
| `EMAIL_HOST_PASSWORD` | fjalëkalimi (për Gmail: "App password") |
| `DEFAULT_FROM_EMAIL` | `DriveOn <info@driveon.al>` |
| `BOOKINGS_EMAIL` | adresa ku vijnë rezervimet e reja |
| `SITE_URL` | `https://driveon.al` (për lidhjet në email) |


## Struktura e projektit

```
projekt-ren-car/
├── car_app/
│   ├── static/
│   │   ├── css/          # style.css, responsive.css
│   │   ├── js/           # script.js, reservation.js
│   │   └── image/        # logo dhe imazhet e faqes
│   ├── templates/        # index, about, cars, explorefleet, contact,
│   │                     # reservation, login, signup, _messages
│   ├── models.py         # Car, Reservation, Review, ContactMessage, Subscriber
│   ├── views.py          # logjika e faqeve
│   ├── forms.py          # format e website-it
│   ├── urls.py           # rrugët e aplikacionit
│   └── admin.py          # konfigurimi i panelit admin
├── media/cars/           # imazhet e ngarkuara të makinave
├── mysite/               # konfigurimi i projektit Django (settings, urls)
├── db.sqlite3            # databaza
└── manage.py
```

## Autori

Projekt i realizuar si pjesë e kursit të Web Development.
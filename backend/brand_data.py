"""
Public information from https://swagatcorner.com/ (outlets, links).
Used in templates via app context processor.
"""

# Primary links
WEBSITE_URL = "https://swagatcorner.com/"
MENU_PDF_URL = "https://swagatcorner.com/images/Swagat_New_Menu.pdf"
WHATSAPP_URL = "https://wa.me/919825122471"

# Storyline from the site hero
TAGLINE_WEB = "Where Every Bite Tells a Delicious Story!"

# Printed menu card line (also used in .env)
TAGLINE_MENU_CARD = "Good Taste, Better Quality, Best Food at Reasonable Rate"

ESTABLISHED_YEAR = "2003"

# Vadodara outlets (from “Visit Us” on the website)
OUTLETS = [
    {
        "name": "Subhanpura",
        "address": "7, Vitthlalesh Avenue, New IPCL Gorwa Road, Subhanpura, Vadodara",
        "maps": "https://g.co/kgs/Dqm9Mp2",
    },
    {
        "name": "Manjalpur",
        "address": "1, Abhishek House, Tulsidham Cross Road, Manjalpur, Vadodara",
        "maps": "https://g.co/kgs/Xotekdv",
    },
    {
        "name": "New VIP Road",
        "address": "1, Neelnandan Complex, Opp. Sadhu Vaswani School, New VIP Road, Vadodara",
        "maps": "https://www.google.com/search?q=Swagat+Corner+New+VIP+Road+Vadodara",
    },
    {
        "name": "Nizampura",
        "address": "GF-8, Dev Deep Complex, B/s. ICICI Bank, Nr. Deluxe Cross Roads, Nizampura, Vadodara",
        "maps": "https://g.co/kgs/4tXEeEi",
    },
    {
        "name": "Waghodia",
        "address": "GF 13-15, Shyam Resi Plaza, Near Parivar Char Rasta, Waghodia Road, Vadodara",
        "maps": "https://g.co/kgs/PJgmXmt",
    },
    {
        "name": "Vasna / Bhayli",
        "address": "GF 22-24, Amraplai Resicom, 30mtr. Sunpharma-Vasna/Bhayli Cross Rd., Vadodara",
        "maps": "https://g.co/kgs/2L8b2mX",
    },
]

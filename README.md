# Communcation Station

An efficient and user friendly online ordering and business management system called the Communcation Station. Powered by Django, Python and a suite of other modern technologies.

## Features
- Intuitive order management using Django's powerful admin interface.
- Data management and MVC powered by Python
- Responsive front-end design using Bootstrap.
- Easy-to-read and interactive UI with HTML & JavaScript.
- Beautiful icons powered by Font Awesome.
- Robust and scalable database system using PostgreSQL.
- Location-based features using the Google Maps API and GDAL.
- Secure payment processing through PayPal.

## Prerequisites
The following requirements must be met:

- [Python](https://www.python.org/downloads/) (3.6 or higher)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [GDAL](https://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries)

## Installation & Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/online-ordering-system.git
    cd online-ordering-system
    ```

2. **Setup Virtual Environment**:
    ```bash
    python -m venv venv
    On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup PostgreSQL**:
   Ensure PostgreSQL is running and create a database for the project.
   Update `DATABASES` settings in `settings.py` with your database credentials.

5. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

   Visit `http://localhost:8000` or `http://127.0.0.1:8000/` in your browser.

## Configuring APIs

1. **Google Maps API**:
   Obtain your API key from the [Google Cloud Console](https://console.cloud.google.com/).
   Insert the key in the relevant place in your settings or frontend code.

2. **PayPal**:
   Ensure you have set up your [PayPal Developer](https://developer.paypal.com/) account. Integrate your client and secret keys as needed for processing transactions.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](LICENSE)

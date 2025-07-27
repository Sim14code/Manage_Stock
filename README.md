# Warehouse Inventory Management

This is a Django-based warehouse inventory management system.

## Features

- Product management (add, edit, list products)
- Stock transactions (stock in/out, transaction history)
- Inventory overview with low/out-of-stock highlighting
- Responsive UI with light/dark mode

## Project Structure

```
mysite/
    manage.py
    config/
        settings.py
        urls.py
        ...
    core/
        models.py
        views.py
        templates/
        ...
    db.sqlite3
```

## Setup

1. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

2. **Apply migrations**  
   ```
   python manage.py migrate
   ```

3. **Run the development server**  
   ```
   python manage.py runserver
   ```

4. **Access the app**  
   Visit [http://localhost:8000/](http://localhost:8000/)

## Notes

- Default database: SQLite (`db.sqlite3`)
- To create an admin user:  
  ```
  python manage.py createsuperuser
  ```


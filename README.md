# ONE9SIX9 Business Operating System (BOS)

A desktop business operating system built with Python and CustomTkinter.

## Requirements

- Python 3.10 or later
- pip

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Project Structure

```
ONE9SIX9-BOS/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md
└── src/
    ├── app.py              # Main window and page routing
    ├── config/
    │   └── theme.py        # Theme colors, fonts, and layout constants
    └── ui/
        ├── components/
        │   ├── dashboard_card.py
        │   ├── header.py
        │   └── sidebar.py
        └── pages/
            ├── base_page.py
            ├── dashboard_page.py
            ├── projects_page.py
            ├── suppliers_page.py
            ├── categories_page.py
            └── expenses_page.py
```

## Features (Foundation)

- Modern dark theme UI
- Left navigation panel with eight sections
- Top header with application name and today's date
- Dashboard page with placeholder metric cards:
  - Income This Month
  - Expenses This Month
  - Net Profit
  - Pending Approvals
- Project management page (add projects from the Excel workbook)
- Supplier management page (add suppliers from the Excel workbook)
- Category management page (add categories from the Excel workbook)
- Expense management page (add expenses from the Excel workbook, with automatic VAT total calculation)

## License

Proprietary — ONE9SIX9

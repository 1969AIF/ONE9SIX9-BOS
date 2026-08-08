# ONE9SIX9 Business Operating System (BOS)

Python/CustomTkinter desktop app. Data is stored in an Excel workbook via openpyxl.

## Commands

- Run: `python main.py`
- Test: `python tests/test_bugfixes.py`
- Dependencies: `pip install -r requirements.txt`

## Architecture

- `main.py` — entry point; initializes `ExcelService`, sets dark theme, launches `MainWindow`
- `src/app.py` — `MainWindow` root window: sidebar + header + page container, routes between pages
- `src/config/theme.py` — `Theme` class with all colors, fonts, sizes (single source of truth; no hardcoded colors elsewhere)
- `src/services/excel_service.py` — `ExcelService` class managing the workbook (`ONE9SIX9.xlsx`). Worksheets: Dashboard, Expenses, Income, Projects, Suppliers, Categories, Settings. Dataclasses: `Project`, `Supplier`
- `src/ui/components/` — `Header`, `Sidebar`, `NewProjectDialog`, `NewSupplierDialog`, `DashboardCard`
- `src/ui/pages/` — `BasePage`, `DashboardPage`, `ProjectsPage`, `SuppliersPage` (each page has `refresh()`)

## Conventions

- Dark theme from `Theme`; never hardcode colors
- Pages use `customtkinter` grid/pack; tables rebuilt in `refresh()` by destroying and re-adding rows
- `ExcelService` is a class-based singleton; call `ExcelService.initialize(project_root)` before use
- New Excel rows are appended after `sheet.max_row`, columns found by header name (see `_find_column`)
- Keep line length ~88; type hints on all functions; docstrings on public methods

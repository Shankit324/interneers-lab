# Interneers Lab: Hexagonal Architecture GET API

This project is a simple Django-based GET API built using **Hexagonal Architecture** (also known as Ports and Adapters). The primary goal of this architecture is to strictly decouple the core business logic from external frameworks, interfaces, and databases.

---

## Layering Strategy

The codebase is intentionally divided into distinct layers to enforce separation of concerns. Django is treated merely as an "external delivery mechanism" rather than the core of the application.

| Layer | Directory | Responsibility | Rules |
| :--- | :--- | :--- | :--- |
| **Domain (Core)** | `core/domain.py` | Contains the pure business rules and logic. | **Zero dependencies** on Django, HTTP, or databases. Pure Python only. |
| **Ports** | `core/ports.py` | Defines the interfaces (contracts) for how the Domain communicates with the outside world. | Uses abstract base classes. |
| **Adapters** | `api/adapters.py` | Acts as the bridge between the external world and the Domain. | Translates HTTP requests into Domain objects and vice versa. |
| **Infrastructure** | `api/views.py` | The entry point for the web framework. | Handles routing and HTTP responses (Django's domain). |

---

## Directory Structure

```text
django_app/
├── core/                # The "Inside"
│   ├── __init__.py
│   ├── domain.py        # Business logic (e.g., GreetingService)
│   └── ports.py         # Interfaces
├── api/                 # The "Outside" & The "Bridge"
│   ├── __init__.py
│   ├── adapters.py      # Request/Response translation
│   └── views.py         # Django HTTP endpoints
└── manage.py
```

---

## Request Flow (How Data Moves)

1. **Client Request:** A user makes a GET request via Postman or browser.

2. **Infrastructure (View):** api/views.py receives the HTTP request and extracts the raw parameters.

3. **Adapter:** The view passes the parameters to api/adapters.py. The adapter sanitizes/formats the data for the domain.

4. **Domain:** The adapter calls the specific service in core/domain.py. The pure logic executes and returns the result to the adapter.

5. **Response:** The adapter hands the formatted result back to the view, which wraps it in a Django JsonResponse and sends it to the client.

---
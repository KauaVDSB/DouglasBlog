[![CI](https://github.com/KauaVDSB/douglasBlog/actions/workflows/ci.yml/badge.svg)](https://github.com/KauaVDSB/douglasBlog/actions/workflows/ci.yml) [![Version](https://img.shields.io/badge/version-1.1.1-blue.svg)](https://github.com/KauaVDSB/douglasBlog/releases/tag/v1.1.1) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# douglasBlog

**Interactive blog platform for physics education, built with Flask and Supabase.**

🔗 **Live Demo:** https://douglaslima.vercel.app

---

## 📑 Table of Contents
- [Features](README.md#-features)
- [Admin Dashboard](README.md#admin-dashboard)
- [Project Structure](README.md#-project-structure)
- [Installation & Configuration](README.md#-installation--configuration)
- [Environment Variables](README.md#-environment-variables)
- [Running the App](README.md#-running-the-app)
- [API Example](README.md#-api-example)
- [Screenshots & GIF](README.md#-screenshots--gif)
- [Deployment](README.md#-deployment)
- [Changelog](README.md#-changelog)
- [License](README.md#-license)
- [Contributing](README.md#-contributing)
- [Author](README.md#-author)
- [PT-BR](README.md#-pt-br)

---

## 🚀 Features
- **CRUD for Posts & Materials:** Create, edit, delete posts and educational materials via Flask-WTF.
- **Dynamic Pagination:** Loads posts per page with `X-Total-Count` header for total count.
- **Supabase Integration:** PostgreSQL database and Storage for media uploads.
- **Advanced Editor:** CKEditor 5 with a **custom plugin** for in-editor image previews and LaTeX rendering via MathJax.
- **Responsive Design:** Modular CSS and componentized JavaScript organized by feature.
- **CI/CD Pipelines:** Automated lint and test workflows in GitHub Actions.

---

## Admin Dashboard

O painel de administração agora conta com:

- **Sidebar fixa** para navegação entre:
  - Gestão de Posts (criação/edição)
  - Gestão de Materiais (criação/edição)
  - Perfil de Usuário
  - Dashboard (visualização de métricas)
- **Dashboard de Analytics**:
  - Gráficos de Visitas Diárias, Semanais e Mensais
  - Filtro por rota diretamente na sidebar

---

## 📁 Project Structure
```bash
.
├── .github/workflows    # CI & lint configurations
├── .vercel              # Vercel deployment settings
├── douglasBlog          # Application package
│   ├── __init__.py      # Flask app factory
│   ├── helpers          # Permission and util modules
│   ├── forms.py         # Flask-WTF form definitions
│   ├── static           # CSS, JS, and media assets
│   └── templates        # Jinja2 HTML templates
├── migrations           # Alembic database migrations
├── .env.example         # Example environment variables
├── .flaskenv            # Flask CLI configuration
├── LICENSE              # MIT License
├── CHANGELOG.md         # Project changelog
├── requirements.txt     # Python dependencies
└── main.py              # Application entry point
```

---

## ⚙️ Installation & Configuration
1. **Clone the repository**
   ```bash
   git clone https://github.com/KauaVDSB/douglasBlog.git
   cd douglasBlog
   ```
2. **Copy and edit environment variables**
   ```bash
   cp .env.example .env
   ```
3. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Apply database migrations**
   ```bash
   flask db upgrade
   ```

---

## 🛠️ Environment Variables
| Variable        | Description                                     |
|-----------------|-------------------------------------------------|
| ACESSO_LOGIN    | Token or flag for login access                  |
| ACESSO_CADASTRO | Token or flag for user registration             |
| DEBUG_MODE      | `'true'` or `'false'` to enable debug logging   |
| DATABASE_URL    | Supabase PostgreSQL connection URL              |
| SUPABASE_URL    | Supabase project URL                            |
| SUPABASE_KEY    | Supabase API key                                |
| SECRET_KEY      | Flask secret key (`app.config['SECRET_KEY']`)   |
| FLASK_ENV       | `'development'` or `'production'`               |

---

## ▶️ Running the App
Start the development server:
```bash
flask run
```
Visit http://127.0.0.1:5000

---

## 📖 API Example
**Front-end (`lista-posts.js`):**
```js
const res = await fetch(`/api/get/lista-posts?page=${page}`);
const posts = await res.json();
posts.forEach(post => { /* render logic */ });
```

**Back-end (`routes.py`):**
```python
@app.route('/api/get/lista-posts')
def api_get_listaPosts():
    page = max(int(request.args.get('page', 1)), 1)
    per_page = 8
    offset = (page-1)*per_page
    query = db.session.query(Postagem.id, Postagem.titulo, Postagem.imagem, Postagem.conteudo)
        .order_by(desc(Postagem.data_postagem)).offset(offset).limit(per_page).all()
    posts = [to_dict(p) for p in query]
    total = db.session.query(func.count(Postagem.id)).scalar()
    response = jsonify(posts)
    response.headers['X-Total-Count'] = total
    return response
```

---

## 📸 Screenshots & GIFs

### Screenshots
| Feature          | Desktop View                                                                                                                                                                        | Mobile View                                                                                                                                                                         |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Posts List       | ![Posts List Desktop](https://github.com/user-attachments/assets/ec37e53b-5382-424f-8c2c-4124c84a3aa7)                                                                               | ![Posts List Mobile](https://github.com/user-attachments/assets/4f6c06f1-cc4f-4d24-b7db-2eb45ecfec6b)                                                                               |
| Post Detail View | ![Post Detail Desktop](https://github.com/user-attachments/assets/6d14277b-5e4b-4cc6-bd9a-b94529e550b9)                                                                              | ![Post Detail Mobile](https://github.com/user-attachments/assets/b07a0d21-2c53-4e64-9d9b-d723b1976f37)                                                                              |

### GIF Demonstrations
| Feature            | Demo                                                                                                                                                                                  |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Loader Animation   | ![Loader GIF](https://github.com/user-attachments/assets/9c055377-e723-456e-800b-a7528c276f9a)                                                                                       |
| Delete Post Flow   | ![Delete GIF](https://github.com/user-attachments/assets/e3c585cc-fcf2-47cf-aa25-37fab487aa63)                                                                                       |


---

## 🚀 Deployment
Live on Vercel: https://douglaslima.vercel.app

---

## 📜 Changelog
See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 📄 License
Distributed under the MIT License. See [LICENSE](LICENSE).

---

## 🤝 Contributing
This is a personal project; external contributions are not accepted at this stage.

---

## ✉️ Author
**KauaVDSB**  
- GitHub: https://github.com/KauaVDSB  
- LinkedIn: https://www.linkedin.com/in/kauã-vinicius-dos-santos-barbosa-346b31344  
- Email: kauavdsb.jobs@gmail.com

---

## PT-BR
**douglasBlog**: Plataforma de blog interativo para educação em física, construída com Flask e Supabase.

### Instalação
Clone o repositório, copie `.env.example` para `.env`, crie/ative venv, instale `pip install -r requirements.txt`, aplique migrações (`flask db upgrade`) e execute `flask run`.

### Uso
Acesse http://127.0.0.1:5000 para visualizar o projeto localmente.

### Licença
Licenciado sob MIT. Veja [LICENSE](LICENSE)


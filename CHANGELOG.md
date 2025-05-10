# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.1.1] – 2025-05-09

### Changed
- Substituídos cards de links para Olimpíadas de Física por **fotos do Professor Douglas**  
- O texto inicial da header foi **dividido em duas partes**, movendo a segunda para dentro da seção “Conteúdos”  
- Pequenas **correções ortográficas** em diversas seções  
- Adicionados **ícones SVG** aos links dinâmicos de Conteúdos


## [1.1.0] – 2025-05-08

### Added
- Nova **sidebar administrativa** com links para todas as seções do admin (Posts, Materiais, Perfil, Dashboard)  
- Incorporação dos **gráficos de analytics** direto em `admin/dashboard.html`  
- Templates de layout exclusivos para o admin em `templates/admin/base/base.html`

### Changed
- Removidos links administrativos antigos de `admin/dashboard.html` e migrados para a sidebar  
- Cada rota administrativa (blog, material, profile) agora estende o layout `admin/base/base.html`  


## [1.0.0] - 2025-04-24
### Added
- Initial stable release of **douglasBlog**.
- CRUD functionalities for posts and materials.
- Pagination with `X-Total-Count` header.
- Integration with Supabase (PostgreSQL & Storage).
- Custom CKEditor 5 plugin for image previews.
- Included DOMPurify via CDN in base template for sanitizing HTML.

### Changed
- Rendered MathJax formulas in post previews on `lista-posts.html`, treating both `\(...\)` and `\[...\]` as inline math.
- Post previews now send HTML snippets (up to 70 characters) with tags (`<strong>`, `<i>`, `<span>`) sanitized using DOMPurify.
- Applied static CSS `line-clamp: 3` and `-webkit-line-clamp: 3` to `.conteudo-post` for consistent preview truncation.

### Fixed
- Minor CSS inconsistencies in mobile responsiveness.
- Registration flow bug that prevented new users from completing signup.


<!-- referências de tag de release -->
[1.1.1]: https://github.com/KauaVDSB/douglasBlog/releases/tag/v1.1.1
[1.1.0]: https://github.com/KauaVDSB/douglasBlog/releases/tag/v1.1.0
[1.0.0]: https://github.com/KauaVDSB/douglasBlog/releases/tag/v1.0.0
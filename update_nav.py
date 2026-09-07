with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace navbar
old_nav = """<li class="nav-item"><a class="nav-link nav-link-manual" href="#dashboard-final"><i class="bi bi-speedometer2"></i> 7. Dashboard Streamlit</a></li>
      </ul>"""

new_nav = """<li class="nav-item"><a class="nav-link nav-link-manual" href="#dashboard-final"><i class="bi bi-speedometer2"></i> 7. Dashboard Streamlit</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link nav-link-manual dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Dashboards PRO</a>
          <ul class="dropdown-menu border-0 shadow">
            <li><a class="dropdown-item" href="#dashboard-api">8. Monitor de Divisas (API)</a></li>
            <li><a class="dropdown-item" href="#dashboard-nlp">9. NLP Sentimientos</a></li>
            <li><a class="dropdown-item" href="#dashboard-geo">10. Rutas y GeoTracking</a></li>
          </ul>
        </li>
      </ul>"""

if old_nav in content:
    content = content.replace(old_nav, new_nav)
    print("Navbar updated.")

# Replace sidebar
old_sidebar = """<a href="#dashboard-final" class="d-block text-dark py-1"><i class="bi bi-speedometer2 text-secondary"></i> 7. Dashboard Final</a>
    </div>"""

new_sidebar = """<a href="#dashboard-final" class="d-block text-dark py-1"><i class="bi bi-speedometer2 text-secondary"></i> 7. Dashboard Final</a>
      <a href="#dashboard-api" class="d-block text-dark py-1"><i class="bi bi-globe text-secondary"></i> 8. Divisas (API)</a>
      <a href="#dashboard-nlp" class="d-block text-dark py-1"><i class="bi bi-chat-text text-secondary"></i> 9. NLP Sentimientos</a>
      <a href="#dashboard-geo" class="d-block text-dark py-1"><i class="bi bi-geo-alt text-secondary"></i> 10. GeoTracking Logística</a>
    </div>"""

if old_sidebar in content:
    content = content.replace(old_sidebar, new_sidebar)
    print("Sidebar updated.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

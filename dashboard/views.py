from django.shortcuts import render
from Usuario.models import Clientes
from Proveedores.models import Proveedores  # Importa el modelo de proveedores
from Inventario.models import Productos  # Importa el modelo de productos
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db import models
from functools import wraps
from .models import AuditLog
from django.utils.timezone import now
from .decorators import log_view_access
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth.backends import ModelBackend
from django.contrib.contenttypes.models import ContentType
from Usuario.models import Clientes
from Proveedores.models import Proveedores
from Inventario.models import Productos

# Asignar el permiso al usuario
# content_type = ContentType.objects.get_for_model(AuditLog)
# permission = Permission.objects.get(codename='view_auditlog', content_type=content_type)
# user = User.objects.get(username='gregory')
# user.user_permissions.add(permission)

# Create your vie
def log_view_access(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        AuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action="ACCESO",
            model_name=view_func.__name__,
            timestamp=now(),
            details=f"Acceso a {view_func.__name__} con args={args} kwargs={kwargs}"
        )
        return view_func(request, *args, **kwargs)
    return wrapper

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Solo usa la autenticación estándar
        return super().form_valid(form)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Cambia 'home' por tu página principal
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def index(request):
    productos = Productos.objects.all()  # Obtener todos los productos
    return render(request, 'index.html', {'productos': productos})

# ESTA VISTA NO DEBE TENER @login_required
def formulario(request):
    return render(request, 'registration/login.html')


def formulario_view(request):
    return render(request, 'registro.html') # Cambia 'registro.html' por la plantilla adecuada.

def registro(request):

    context = {
        'racismo': 'FerreElectri PLUS | Registro'
    }

    return render(request, 'registro.html', context)

def recuperar(request):

    context = {
        'racismo': 'FerreElectri PLUS | Recuperar'
    }

    return render(request, 'recuperar.html', context)

@login_required
def dashboard(request):
    logs = AuditLog.objects.all().order_by('-timestamp')[:10]
    clientes_nuevos = Clientes.objects.count()
    proveedores_nuevos = Proveedores.objects.count()
    productos_nuevos = Productos.objects.count()
    context = {
        'racismo': 'FerreElectri PLUS | Dashboard',
        'audit_logs': logs,
        'clientes_nuevos': clientes_nuevos,
        'proveedores_nuevos': proveedores_nuevos,
        'productos_nuevos': productos_nuevos,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
@log_view_access
def clientes(request):
    query = request.GET.get('q', '')
    clientes_qs = Clientes.objects.all().order_by('-fecha_registro')
    if query:
        clientes_qs = clientes_qs.filter(
            models.Q(nombre__icontains=query) |
            models.Q(apellido__icontains=query) |
            models.Q(telefono__icontains=query) |
            models.Q(cedula__icontains=query)
        )
    clientes = clientes_qs[:5]

    contador_nuevo = Clientes.objects.count()
    contador_nuevo2 = Clientes.objects.filter(frecuente=True).count()
    contador_nuevo3 = Clientes.objects.filter(vip=True).count()

    context = {
        'racismo': 'FerreElectri PLUS | Clientes',
        'clientes': clientes,
        'clientes_nuevos': contador_nuevo,
        'cliente_frecuente': contador_nuevo2,
        'cliente_vip': contador_nuevo3,
    }
    return render(request, 'clientes.html', context)

@login_required
@log_view_access
def proveedores(request):
    query = request.GET.get('q', '')
    proveedores_qs = Proveedores.objects.all().order_by('-Fecha_registro')
    if query:
        proveedores_qs = proveedores_qs.filter(
            models.Q(Nombre__icontains=query) |
            models.Q(Apellido__icontains=query) |
            models.Q(Telefono__icontains=query) |
            models.Q(Cedula__icontains=query)
        )
    proveedores = proveedores_qs[:5]
    contador_nuevo_p = Proveedores.objects.count()

    context = {
        'racismo': 'FerreElectri PLUS | Proveedores',
        'proveedores': proveedores,
        'proveedores_nuevos': contador_nuevo_p,
    }
    return render(request, 'proveedores.html', context)

@login_required
@log_view_access
def inventario(request):
    query = request.GET.get('q', '')
    productos_qs = Productos.objects.all().order_by('-Fecha_creacion')
    if query:
        productos_qs = productos_qs.filter(
            models.Q(Codigo__icontains=query) |
            models.Q(Nombre__icontains=query) |
            models.Q(Precio__icontains=query) |
            models.Q(Cantidad__icontains=query) |
            models.Q(Fecha_creacion__icontains=query)
        )
    productos = productos_qs[:5]
    contador_nuevo_1 = Productos.objects.count()
    contador_nuevo_2 = Productos.objects.filter(promocion=True).count()

    context = {
        'racismo': 'FerreElectri PLUS | Inventario',
        'productos': productos,
        'productos_nuevos': contador_nuevo_1,
        'productos_promocion': contador_nuevo_2,
        'query': query,
    }

    return render(request, 'inventario.html', context)

@login_required
@permission_required('dashboard.view_auditlog')
def audit_logs(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'audit_logs.html', {'logs': logs})
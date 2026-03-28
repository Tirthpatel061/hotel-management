"""Route decorators for role-based access."""
from functools import wraps
from flask import abort
from flask_login import current_user


def roles_required(*allowed_roles):
    """Allow only users whose role is in allowed_roles."""

    def decorator(view_fn):
        @wraps(view_fn)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in allowed_roles:
                abort(403)
            return view_fn(*args, **kwargs)

        return wrapped

    return decorator

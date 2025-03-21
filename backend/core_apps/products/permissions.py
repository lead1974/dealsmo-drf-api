from rest_framework import permissions


class ProductPermission(permissions.BasePermission):
    """
    Custom permission class for Product model.
    - Anyone can view products
    - Only authenticated users can create products
    - Users can only edit/delete their own products
    - Staff members can edit/delete any product
    """
    
    def has_permission(self, request, view):
        # Allow read operations for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Require authentication for write operations
        if not request.user.is_authenticated:
            return False
            
        # Staff members have full access
        if request.user.is_staff:
            return True
            
        # Check specific permissions for different operations
        if request.method == 'POST':
            return request.user.has_perm('products.can_create_product')
        elif request.method in ['PUT', 'PATCH']:
            return request.user.has_perm('products.can_edit_product')
        elif request.method == 'DELETE':
            return request.user.has_perm('products.can_delete_product')
            
        return False

    def has_object_permission(self, request, view, obj):
        # Allow read operations for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Require authentication for write operations
        if not request.user.is_authenticated:
            return False
            
        # Staff members have full access
        if request.user.is_staff:
            return True
            
        # Users can only edit/delete their own products
        if obj.author == request.user:
            if request.method in ['PUT', 'PATCH']:
                return request.user.has_perm('products.can_edit_product')
            elif request.method == 'DELETE':
                return request.user.has_perm('products.can_delete_product')
            
        return False 
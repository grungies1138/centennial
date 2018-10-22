"""
Vendor requirements:

    Vendors will allow for the sale of items on the grid.  This can come in two forms.  Either 'real' items loaded into
    the vendors object or from a list of prototypes.  This should appear seamless to the buyer.

    Vendors should be able to accept either a list of prototypes or the possibility of listing all prototypes from a
    specific manufacturer.  (manufacturer is an attribute on the prototypes.)

    Use EvMenu to handle the buying and management interface.  Buyers should be able to view items for sale by category.
    sellers should be able to collect earned income, get items (drop for already built items or discounted price for
    prototyped items), manage what is sold, set prices.

    Seller menu branch should be restricted only to the owner of the vendor, authorized users and admins.
"""
"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

    cart = session.get("cart", {})
    # session.get("cart", {}) Explanation
    # Here, we are checking to see if session has a key named, "cart". If it doesn't,
    # then it will create an empty dictionary and put it in the cart variable.
    melons_ordered = []
    order_total = 0

    for melon_id, count in cart.items():
        # To retrieve the Melon object corresponding to this id
        melon = melons.get_by_id(melon_id)
        total_cost = count * melon.price
        order_total += total_cost
        
        melon.count = count
        melon.total_cost = total_cost


        melons_ordered.append(melon)

    return render_template("cart.html",
                           cart=melons_ordered,
                           order_total=order_total)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    if 'cart' not in session:
        # session is a dictionary. Here session looks like this:
        # session = {'cart': {melon_id: count}}
        # session["cart"] = {melon_id: count}
        # so this session dictionary looks like
        # {"cart": {melon_id: count}} - a dictionary with key == "cart" and 
        # and it's value is a dictionary, {melon_id:count}
        # 'cart' in session is to check if the key, 'cart', exists in session
        session['cart'] = {}

    session['cart'][melon_id] = session['cart'].get(melon_id, 0) + 1
    # session['cart'].get(melon_id, 0) explanation:
    # 1) .get method's 1st argument is a key. session['cart'] is a dictionary, {melon_id: count}
    #    the key for session['cart'] is melon_id
    # 2) .get method's 2nd argument is optional, which is a fall back value to return if melon_id
    #    doesn't exist. So it is checking to see if there is any melon_id in the dictionary. If
    #    not, then, it will set the value for melon_id to 0 

    flash("Melon Successfully added to cart!")

    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

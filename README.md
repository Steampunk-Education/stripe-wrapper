# stripe-wrapper
Custom wrapper for the Stripe API. Steampunk employees need a way to generate Stripe Checkout links given the number of hours they have worked, and their rate. That way they can send one-time payment links to education centres with very little overhead. 

This wrapper provides abstracts the Stripe API call; it generates a link given two parameters: `hours` and `rate`;

Example:
```
GET /v1/link?hours=5.0&rate=5.0
```
Returns `{"link":<payment link>}`
> `hours` and `rate` can are required parameters and can be passed in as integers or floating point numbers.

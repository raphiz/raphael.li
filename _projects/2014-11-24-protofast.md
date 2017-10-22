---
layout: project
title: Protofast
type: experiment
github: https://github.com/raphiz/protofast
teaser: Quickly create HTML mock-ups without duplicating code
initiation: 2014
status: inactive
---
Protofast is an easy to use solution to quickly create ambitious HTML mock-up websites with PHP.

I use this to design a plain HTML layout before I start to write any code. The project's stakeholder can play around with this prototype and give instant feedback concerning the UI. Experiments with new UI-Concepts are cheaper this way. When the final draft is accepted by all parties, the actual implementation begins.

To be honest, there are easier ways to build interactive html mock-ups - probably with frameworks or tools that you are more familiar with.
This project was not created to serve a wide audience - it was primarily a task to sharpen my PHP skills.

## An example

Let's take a look at a practical example on how Protofast works:

Therefore, let's create a basic `index.php`

```php
<?php
// Require the Protofast framework
require_once "vendor/protofast.php";

// Create a new "Site"
$site = new protofast\HTMLPage();

// Set a title for the site and declare some additional scripts and
// stylesheets
$site->setTitle("Home");
$site->addStylesheet("stylesheets/specific_index.css");
$site->addScript("stylesheets/index_only.js");

// Render the site
$site->render();
```

As you can see, you can declare custom style sheets, scripts and other properties in a readable and maintainable fashion.

Let's take a look on the template part. Templates are located in the `templates/` folder relative to the `index.php` file.
There must be a file called `base.html` which is - you guess it - the base of every template.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My awesome website - {{PAGE_TITLE}}</title>
    <meta name="description" content="{{PAGE_DESCRIPTION}}">

    <link rel="stylesheet" type="text/css" href="stylesheets/base.css">
    {{STYLESHEETS}}

    <script type="text/javascript" src="js/base.js"></script>
    {{SCRIPTS}}

  </head>
  <body>
    <div class="fixed_header">
      <h1>My awesome website</h1>
    </div>
    <div class="content">
      {{CONTENT}}
    </div>
  </body>
</html>
```

Each site extends this  `base.html` file. We can specify an `index.html` template for our example `index.php` file within the `template/` folder.

```html
<h2>Howdy!</h1>
<p>Welcome! This is the index!</p>
<p>Do also check out the <a href="example.php">Example</a> page!</p>
```

Checkout the full example project and more documentation on [Github](https://github.com/raphiz/protofast/tree/master/example_project).

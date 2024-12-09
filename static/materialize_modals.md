Use a modal for dialog boxes, confirmation messages, or other content that can be called up. In order for the modal to work you have to add the Modal ID to the link of the trigger. To add a close button, just add the class .modal-close to your button.

<!-- Modal Trigger -->
```html
<a class="waves-effect waves-light btn modal-trigger" href="#modal1">Modal</a>

<!-- Modal Structure -->
<div id="modal1" class="modal">
<div class="modal-content">
    <h4>Modal Header</h4>
    <p>A bunch of text</p>
</div>
<div class="modal-footer">
    <a href="#!" class="modal-close waves-effect waves-green btn-flat">Agree</a>
</div>
</div>
```

<!-- Modal Trigger -->
```html
<button data-target="modal1" class="btn modal-trigger">Modal</button>
```
Initialization
```js
document.addEventListener('DOMContentLoaded', function() {
var elems = document.querySelectorAll('.modal');
var instances = M.Modal.init(elems, options);
});
```

Options
You can customize the behavior of each modal using these options. For example, you can call a custom function to run when a modal is dismissed. To do this, just place your function in the intialization code as shown below.

Name	Type	Default	Description
opacity	Number	0.5	Opacity of the modal overlay.
inDuration	Number	250	Transition in duration in milliseconds.
outDuration	Number	250	Transition out duration in milliseconds.
onOpenStart	Function	null	Callback function called before modal is opened.
onOpenEnd	Function	null	Callback function called after modal is opened.
onCloseStart	Function	null	Callback function called before modal is closed.
onCloseEnd	Function	null	Callback function called after modal is closed.
preventScrolling	Boolean	true	Prevent page from scrolling while modal is open.
dismissible	Boolean	true	Allow modal to be dismissed by keyboard or overlay click.
startingTop	String	'4%'	Starting top offset
endingTop	String	'10%'	Ending top offset

Methods
Because jQuery is no longer a dependency, all the methods are called on the plugin instance. You can get the plugin instance like this:

```js
var instance = M.Modal.getInstance(elem);

instance.open();
instance.close();
instance.destroy();
```

Properties
Name	Type	Description
el	Element	The DOM element the plugin was initialized with.
options	Object	The options the instance was initialized with.
isOpen	Boolean	If the modal is open.
id	string	ID of the modal element


If you have content that is very long and you want the action buttons to be visible all the time, you can add the modal-fixed-footer class to the modal.

```html
<!-- Modal Trigger -->
<a class="waves-effect waves-light btn modal-trigger" href="#modal1">Modal</a>

<!-- Modal Structure -->
<div id="modal1" class="modal modal-fixed-footer">
<div class="modal-content">
    <h4>Modal Header</h4>
    <p>A bunch of text</p>
</div>
<div class="modal-footer">
    <a href="#!" class="modal-close waves-effect waves-green btn-flat">Agree</a>
</div>
</div>
```

# Item Value History Plugin

Plugin to store historical values of an Item in an child Item called `history_item`.


## Requirements
No special requirements.

## Configuration

### plugin.yaml
Add the plugin to `plugin.yaml` to activate the plugin.

```
history:
    class_name: ItemHistory
    class_path: plugins.itemhistory.history

```
### items.yaml
Add to an Item the `history: <size>` Parameter.

`<size>` defines the number of values stored in the history_item. Don't make it to large.
If the value of `history` can not be parsed, the global value from `plugin.yaml` is used.
Is there no global size definition in `plugin.yaml` and no size in the Item, the plugin set it to `5`




```
numitem:
    type: str
    history: 6
    cache: True
```


## Usage:



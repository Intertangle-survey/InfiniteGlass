#ifndef ITEM_WINDOW
#define ITEM_WINDOW

#include "item.h"
#include "texture.h"
#include "property.h"

typedef struct {
  Item base;

  int x;
  int y;
  Window window;

  int width_property;
  int height_property;
  int width_window;
  int height_window;

  List *properties;
  Property *prop_size;
  Property *prop_coords;
} ItemWindow;

extern ItemType item_type_window;

extern void item_type_window_update_space_pos_from_window(ItemWindow *item);
extern Item *item_get_from_window(Window window, int create);
extern void items_get_from_toplevel_windows();

#endif

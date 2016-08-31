//Place in plugins folder

object_event_add(CollisionMapO, ev_create, 0,"
visible = 1;
image_alpha = 0;
setVisibility = 0;
")


object_event_add(CollisionMapO, ev_step, 0,"
if keyboard_check_pressed(ord('O')) then setVisibility += 1;
if setVisibility > 1 then setVisibility = 0;


if image_alpha < setVisibility then image_alpha += 0.1;
if image_alpha > setVisibility then image_alpha -= 0.1;
")
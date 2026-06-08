package com.fyt7862.clock;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.SharedPreferences;
import android.widget.RemoteViews;
public class ClockWidget extends AppWidgetProvider {
  // Global defaults: lavender text + purple-gray pill (7870 match), ~80% opacity.
  static final int DEF_TEXT = 0xFFC8BFFF;
  static final int DEF_BG   = 0xFF312E41;
  static final int DEF_BGA  = 204;
  static SharedPreferences prefs(Context c) { return c.getSharedPreferences("clk", Context.MODE_PRIVATE); }
  static void update(Context ctx, AppWidgetManager mgr, int id) {
    SharedPreferences p = prefs(ctx);
    int textColor = p.getInt("text", DEF_TEXT);
    int bgColor   = p.getInt("bg",   DEF_BG);
    int bgAlpha   = p.getInt("bga",  DEF_BGA);
    RemoteViews v = new RemoteViews(ctx.getPackageName(), R.layout.clock_widget);
    v.setTextColor(R.id.hour, textColor);
    v.setTextColor(R.id.minute, textColor);
    v.setTextColor(R.id.date, textColor);
    v.setInt(R.id.bg, "setColorFilter", bgColor);
    v.setInt(R.id.bg, "setImageAlpha", bgAlpha);
    mgr.updateAppWidget(id, v);
  }
  static void updateAll(Context ctx) {
    AppWidgetManager mgr = AppWidgetManager.getInstance(ctx);
    int[] ids = mgr.getAppWidgetIds(new ComponentName(ctx, ClockWidget.class));
    for (int id : ids) update(ctx, mgr, id);
  }
  public void onUpdate(Context ctx, AppWidgetManager mgr, int[] ids) {
    for (int id : ids) update(ctx, mgr, id);
  }
}

package com.fyt7862.clock;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.SharedPreferences;
import android.widget.RemoteViews;
public class ClockWidget extends AppWidgetProvider {
  static void update(Context ctx, AppWidgetManager mgr, int id) {
    SharedPreferences p = ctx.getSharedPreferences("clk", Context.MODE_PRIVATE);
    int color = p.getInt("c_" + id, 0xFFFFFFFF);
    RemoteViews v = new RemoteViews(ctx.getPackageName(), R.layout.clock_widget);
    v.setTextColor(R.id.hour, color);
    v.setTextColor(R.id.minute, color);
    v.setTextColor(R.id.date, color);
    mgr.updateAppWidget(id, v);
  }
  public void onUpdate(Context ctx, AppWidgetManager mgr, int[] ids) {
    for (int id : ids) update(ctx, mgr, id);
  }
}

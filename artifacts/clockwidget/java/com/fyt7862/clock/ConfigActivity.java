package com.fyt7862.clock;
import android.app.Activity;
import android.appwidget.AppWidgetManager;
import android.content.Intent;
import android.os.Bundle;
public class ConfigActivity extends Activity {
  // On add, apply the current global style and finish. Colors are tuned
  // anytime from the "FYT Clock" launcher entry (PreviewActivity).
  public void onCreate(Bundle b) {
    super.onCreate(b);
    int widgetId = AppWidgetManager.INVALID_APPWIDGET_ID;
    Bundle ex = getIntent().getExtras();
    if (ex != null) widgetId = ex.getInt(AppWidgetManager.EXTRA_APPWIDGET_ID, widgetId);
    if (widgetId == AppWidgetManager.INVALID_APPWIDGET_ID) { finish(); return; }
    ClockWidget.update(this, AppWidgetManager.getInstance(this), widgetId);
    Intent r = new Intent();
    r.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, widgetId);
    setResult(RESULT_OK, r);
    finish();
  }
}

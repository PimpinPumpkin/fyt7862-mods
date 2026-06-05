package com.fyt7862.clock;
import android.app.Activity;
import android.appwidget.AppWidgetManager;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
public class ConfigActivity extends Activity {
  int widgetId = AppWidgetManager.INVALID_APPWIDGET_ID;
  final int[] colors = {0xFFFFFFFF, 0xFF71B5FF, 0xFFFF5252, 0xFF69F0AE, 0xFFFFD740, 0xFFB388FF};
  public void onCreate(Bundle b) {
    super.onCreate(b);
    setResult(RESULT_CANCELED);
    Bundle ex = getIntent().getExtras();
    if (ex != null) widgetId = ex.getInt(AppWidgetManager.EXTRA_APPWIDGET_ID, widgetId);
    if (widgetId == AppWidgetManager.INVALID_APPWIDGET_ID) { finish(); return; }
    setContentView(R.layout.config);
    LinearLayout row = (LinearLayout) findViewById(R.id.row);
    for (final int c : colors) {
      Button btn = new Button(this);
      btn.setBackgroundColor(c);
      LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(84, 84);
      lp.setMargins(7, 7, 7, 7);
      btn.setLayoutParams(lp);
      btn.setOnClickListener(new View.OnClickListener() { public void onClick(View v) { pick(c); } });
      row.addView(btn);
    }
  }
  void pick(int color) {
    getSharedPreferences("clk", MODE_PRIVATE).edit().putInt("c_" + widgetId, color).apply();
    ClockWidget.update(this, AppWidgetManager.getInstance(this), widgetId);
    Intent r = new Intent();
    r.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, widgetId);
    setResult(RESULT_OK, r);
    finish();
  }
}

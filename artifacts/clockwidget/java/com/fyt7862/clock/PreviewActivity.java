package com.fyt7862.clock;
import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.PorterDuff;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.SeekBar;
import android.widget.TextClock;
import android.widget.TextView;
import android.widget.EditText;

public class PreviewActivity extends Activity {
  final int[] textColors = {0xFFFFFFFF, 0xFFB69DF8, 0xFF71B5FF, 0xFFD0D0D0, 0xFFFF5252, 0xFF69F0AE, 0xFFFFD740, 0xFF202020};
  final int[] bgColors   = {0xFF0E0F13, 0xFF191919, 0xFF2C2C34, 0xFF1A2438, 0xFF4A72B8, 0xFFB69DF8, 0xFF000000, 0xFFFFFFFF};
  ImageView bgView; TextClock h, m, d;

  int dp(int v){ return (int)(v*getResources().getDisplayMetrics().density + 0.5f); }
  SharedPreferences prefs(){ return ClockWidget.prefs(this); }

  protected void onCreate(Bundle b) {
    super.onCreate(b);
    ScrollView sc = new ScrollView(this);
    sc.setBackgroundColor(0xFF0a0b10);
    LinearLayout root = new LinearLayout(this);
    root.setOrientation(LinearLayout.VERTICAL);
    root.setPadding(dp(20),dp(20),dp(20),dp(20));
    sc.addView(root);

    FrameLayout preview = new FrameLayout(this);
    preview.setBackgroundColor(0xFF0a0b10);
    preview.setPadding(dp(16),dp(24),dp(16),dp(24));
    LinearLayout.LayoutParams pl = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    pl.bottomMargin = dp(18); preview.setLayoutParams(pl);
    View w = getLayoutInflater().inflate(R.layout.clock_widget, preview, false);
    FrameLayout.LayoutParams wl = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
    wl.gravity = Gravity.CENTER; preview.addView(w, wl);
    bgView = (ImageView) w.findViewById(R.id.bg);
    h = (TextClock) w.findViewById(R.id.hour);
    m = (TextClock) w.findViewById(R.id.minute);
    d = (TextClock) w.findViewById(R.id.date);
    root.addView(preview);

    root.addView(label("Text color"));
    root.addView(swatchRow(textColors, true));
    root.addView(label("Background color"));
    root.addView(swatchRow(bgColors, false));
    root.addView(label("Background opacity"));
    root.addView(opacityBar());
    root.addView(label("Text color — hex"));
    root.addView(hexRow(true));
    root.addView(label("Background color — hex"));
    root.addView(hexRow(false));

    setContentView(sc);
    apply();
  }

  TextView label(String s){
    TextView t = new TextView(this);
    t.setText(s); t.setTextColor(0xFFE0E0E0); t.setTextSize(15);
    t.setPadding(0,dp(12),0,dp(8));
    return t;
  }

  LinearLayout swatchRow(final int[] cols, final boolean isText){
    LinearLayout row = new LinearLayout(this);
    row.setOrientation(LinearLayout.HORIZONTAL);
    for (final int c : cols){
      Button btn = new Button(this);
      btn.setBackgroundColor(c);
      btn.setMinWidth(0); btn.setMinHeight(0); btn.setMinimumWidth(0); btn.setMinimumHeight(0);
      btn.setPadding(0,0,0,0);
      LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(dp(38),dp(38));
      lp.setMargins(dp(4),dp(4),dp(4),dp(4)); btn.setLayoutParams(lp);
      btn.setOnClickListener(new View.OnClickListener(){ public void onClick(View v){
        prefs().edit().putInt(isText?"text":"bg", c).apply(); apply();
      }});
      row.addView(btn);
    }
    return row;
  }

  SeekBar opacityBar(){
    SeekBar sb = new SeekBar(this);
    sb.setMax(255);
    sb.setProgress(prefs().getInt("bga", ClockWidget.DEF_BGA));
    sb.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
      public void onProgressChanged(SeekBar s,int p,boolean u){ prefs().edit().putInt("bga",p).apply(); apply(); }
      public void onStartTrackingTouch(SeekBar s){}
      public void onStopTrackingTouch(SeekBar s){}
    });
    return sb;
  }

  void apply(){
    SharedPreferences p = prefs();
    int t = p.getInt("text", ClockWidget.DEF_TEXT);
    int bg = p.getInt("bg", ClockWidget.DEF_BG);
    int a = p.getInt("bga", ClockWidget.DEF_BGA);
    h.setTextColor(t); m.setTextColor(t); d.setTextColor(t);
    bgView.setColorFilter(bg, PorterDuff.Mode.SRC_ATOP);
    bgView.setImageAlpha(a);
    ClockWidget.updateAll(this);
  }

  // Free-form hex entry for arbitrary colors (text or background).
  LinearLayout hexRow(final boolean isText){
    LinearLayout row = new LinearLayout(this);
    row.setOrientation(LinearLayout.HORIZONTAL);
    row.setGravity(Gravity.CENTER_VERTICAL);
    final EditText et = new EditText(this);
    et.setHint("#RRGGBB or #AARRGGBB");
    et.setTextColor(0xFFFFFFFF); et.setHintTextColor(0xFF707070);
    et.setSingleLine(true);
    int cur = prefs().getInt(isText?"text":"bg", isText?ClockWidget.DEF_TEXT:ClockWidget.DEF_BG);
    et.setText(String.format("#%08X", cur));
    LinearLayout.LayoutParams el = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
    et.setLayoutParams(el);
    Button set = new Button(this);
    set.setText("Set");
    set.setOnClickListener(new View.OnClickListener(){ public void onClick(View v){
      Integer c = parseHex(et.getText().toString());
      if (c==null){ et.setError("Use #RRGGBB or #AARRGGBB"); return; }
      et.setText(String.format("#%08X", c));
      prefs().edit().putInt(isText?"text":"bg", c).apply(); apply();
    }});
    row.addView(et); row.addView(set);
    return row;
  }

  Integer parseHex(String s){
    if (s==null) return null;
    s = s.trim(); if (s.startsWith("#")) s = s.substring(1);
    try {
      if (s.length()==6) return (int)(0xFF000000L | Long.parseLong(s,16));
      if (s.length()==8) return (int)(Long.parseLong(s,16));
    } catch (Exception e){}
    return null;
  }
}

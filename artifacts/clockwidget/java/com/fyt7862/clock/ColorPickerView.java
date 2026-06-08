package com.fyt7862.clock;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.RectF;
import android.graphics.Shader;
import android.view.MotionEvent;
import android.view.View;

/** Visual color picker: a saturation/value square + a hue bar underneath. */
public class ColorPickerView extends View {
  public interface OnColor { void onColor(int color); }

  private OnColor listener;
  private final float[] hsv = {280f, 0.55f, 0.85f};
  private final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
  private final RectF sv = new RectF(), hue = new RectF();
  private Shader hueShader, satShader, valShader;
  private int hueH, gap;

  public ColorPickerView(Context c) { super(c); }
  public void setListener(OnColor l) { listener = l; }
  public void setColor(int c) { Color.colorToHSV(c | 0xFF000000, hsv); rebuild(); invalidate(); }
  public int getColor() { return Color.HSVToColor(hsv); }

  private int dp(int v) { return (int)(v * getResources().getDisplayMetrics().density + 0.5f); }

  @Override protected void onSizeChanged(int w, int h, int ow, int oh) {
    hueH = dp(26); gap = dp(14);
    sv.set(0, 0, w, h - hueH - gap);
    hue.set(0, h - hueH, w, h);
    rebuild();
  }

  private void rebuild() {
    if (hue.width() <= 0) return;
    int[] hues = new int[7];
    for (int i = 0; i < 7; i++) hues[i] = Color.HSVToColor(new float[]{i * 60f, 1f, 1f});
    hueShader = new LinearGradient(hue.left, 0, hue.right, 0, hues, null, Shader.TileMode.CLAMP);
    int hueColor = Color.HSVToColor(new float[]{hsv[0], 1f, 1f});
    satShader = new LinearGradient(sv.left, 0, sv.right, 0, Color.WHITE, hueColor, Shader.TileMode.CLAMP);
    valShader = new LinearGradient(0, sv.top, 0, sv.bottom, 0x00000000, 0xFF000000, Shader.TileMode.CLAMP);
  }

  @Override protected void onDraw(Canvas c) {
    if (sv.width() <= 0) return;
    // SV square
    p.setShader(satShader); c.drawRoundRect(sv, dp(6), dp(6), p);
    p.setShader(valShader); c.drawRoundRect(sv, dp(6), dp(6), p);
    p.setShader(null);
    float cx = sv.left + hsv[1] * sv.width();
    float cy = sv.top + (1f - hsv[2]) * sv.height();
    p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(dp(2));
    p.setColor(Color.BLACK); c.drawCircle(cx, cy, dp(8), p);
    p.setColor(Color.WHITE); c.drawCircle(cx, cy, dp(7), p);
    // hue bar
    p.setStyle(Paint.Style.FILL); p.setShader(hueShader);
    c.drawRoundRect(hue, dp(6), dp(6), p); p.setShader(null);
    float hx = hue.left + (hsv[0] / 360f) * hue.width();
    p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(dp(3));
    p.setColor(Color.BLACK); c.drawRect(hx - dp(3), hue.top - dp(2), hx + dp(3), hue.bottom + dp(2), p);
    p.setColor(Color.WHITE); c.drawRect(hx - dp(2), hue.top - dp(2), hx + dp(2), hue.bottom + dp(2), p);
    p.setStyle(Paint.Style.FILL);
  }

  @Override public boolean onTouchEvent(MotionEvent e) {
    float x = e.getX(), y = e.getY();
    if (e.getAction() == MotionEvent.ACTION_DOWN) getParent().requestDisallowInterceptTouchEvent(true);
    if (e.getAction() != MotionEvent.ACTION_CANCEL) {
      if (y <= sv.bottom + gap / 2f) {
        hsv[1] = clamp((x - sv.left) / sv.width());
        hsv[2] = 1f - clamp((y - sv.top) / sv.height());
      } else {
        hsv[0] = clamp((x - hue.left) / hue.width()) * 360f;
        rebuild();
      }
      if (listener != null) listener.onColor(getColor());
      invalidate();
    }
    return true;
  }

  private float clamp(float v) { return v < 0 ? 0 : (v > 1 ? 1 : v); }
}

package com.fyt7862.clock;
import android.app.Activity;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.FrameLayout;
public class PreviewActivity extends Activity {
  protected void onCreate(Bundle b) {
    super.onCreate(b);
    FrameLayout root = new FrameLayout(this);
    root.setBackgroundColor(0xFF0a0b10);
    getLayoutInflater().inflate(R.layout.clock_widget, root);
    View child = root.getChildAt(0);
    FrameLayout.LayoutParams lp = (FrameLayout.LayoutParams) child.getLayoutParams();
    lp.gravity = Gravity.CENTER;
    child.setLayoutParams(lp);
    setContentView(root);
  }
}

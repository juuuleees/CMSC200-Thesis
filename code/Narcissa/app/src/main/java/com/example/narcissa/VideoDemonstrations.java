package com.example.narcissa;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContract;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.media.MediaMetadataRetriever;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import java.io.File;

public class VideoDemonstrations extends AppCompatActivity {

    private Button select_video;
    private MediaMetadataRetriever data_retriever;
    private Uri video_uri;
    private final int SELECT_VIDEO_REQUEST = 100;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.video_demonstrations);

//      Select a video from gallery
        Intent vid_intent = set_retrieval_intent();

        ActivityResultLauncher<Intent> launch_video_demo = registerForActivityResult(
                new ActivityResultContracts.StartActivityForResult(),
                new ActivityResultCallback<ActivityResult>() {
                    @Override
                    public void onActivityResult(ActivityResult result) {
                        if (result.getResultCode() == Activity.RESULT_OK) {
                            Log.i("what", "di ko gets nangyayari but anyway result: " + result.toString());
                            data_retriever = new MediaMetadataRetriever();
//                          Have to call getData() twice to get to the actual content, otherwise proceed as usual
                            video_uri = result.getData().getData();
                            data_retriever.setDataSource(getApplicationContext(), video_uri);
                            VideoMirrorDetection mirror_detector = new VideoMirrorDetection(data_retriever, video_uri);
                            mirror_detector.add_fov();
                        }
                    }
                }
        );

        //      Initialize video selection button
        select_video = (Button)findViewById(R.id.select_video_button);
        select_video.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                launch_video_demo.launch(vid_intent);
            }
        });

    }

    public Intent set_retrieval_intent() {
        Intent intent;
        if (android.os.Environment.getExternalStorageState().equals(Environment.MEDIA_MOUNTED)) {
//          Everything can access external storage
            intent = new Intent(Intent.ACTION_PICK,
                    MediaStore.Video.Media.EXTERNAL_CONTENT_URI);
        } else {
//          Only the app/system/super processes can access internal storage
            intent = new Intent(Intent.ACTION_PICK,
                    MediaStore.Video.Media.INTERNAL_CONTENT_URI);
        }

        intent.setType("video/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);

        return intent;
    }

}
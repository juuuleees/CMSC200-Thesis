package com.example.narcissa;

import android.content.Intent;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

public class Landscape_Frag extends Fragment implements View.OnClickListener {

    private Button video_demo;
    private Button bot_connect;

    public Landscape_Frag() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View landscape_view = inflater.inflate(R.layout.landscape_frag, container, false);
//        Remember that findViewById() needs to be attached to the view na gagamitin mo
        video_demo = (Button)landscape_view.findViewById(R.id.vid_demo);
        bot_connect = (Button)landscape_view.findViewById(R.id.bot_connect);

        video_demo.setOnClickListener(this);
        bot_connect.setOnClickListener(this);

        return landscape_view;
    }

    @Override
    public void onClick(View v) {
        int id = v.getId();
        switch (id) {
            case R.id.vid_demo:
                access_video_demo(v);
                break;
            case R.id.bot_connect:
                connect_bot(v);
                break;
            default:
                break;
        }

    }

    public void access_video_demo(View view) {
//        getActivity() gets the the activity that the fragment's connected to
        Intent intent = new Intent(getActivity(), VideoDemonstrations.class);
        startActivity(intent);
    }

    public void connect_bot(View view) {
        Intent intent = new Intent(getActivity(), BotConnector.class);
        startActivity(intent);
    }

}
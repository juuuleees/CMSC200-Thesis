package com.example.narcissa;

import android.content.Intent;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

public class Portrait_Frag extends Fragment implements View.OnClickListener {

    private Button video_demo;
    private Button connect_bot;

    public Portrait_Frag() {
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
        View portrait_view = inflater.inflate(R.layout.portrait_frag, container, false);
//        Remember that findViewById() needs to be attached to the view na gagamitin mo
        video_demo = (Button)portrait_view.findViewById(R.id.vid_demo);
        connect_bot = (Button)portrait_view.findViewById(R.id.bot_connect);
        video_demo.setOnClickListener(this);
        connect_bot.setOnClickListener(this);

        return portrait_view;
    }

    @Override
    public void onClick(View v) {
        int id = v.getId();
        switch (id) {
            case R.id.vid_demo:
                access_video_demo(v);
                break;
            case R.id.bot_connect:
                connect_to_bot(v);
                break;
            default:
                break;
        }
    }

    public void connect_to_bot(View view) {
        Intent intent = new Intent(getActivity(), BotConnector.class);
        startActivity(intent);
    }

    public void access_video_demo(View view) {
//        getActivity() gets the the activity that the fragment's connected to
        Intent intent = new Intent(getActivity(), VideoDemonstrations.class);
        startActivity(intent);
    }



}
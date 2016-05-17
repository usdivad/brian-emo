/*
 *
 * EMO MUSIC
 *
 */

// emotion stuff
["happy", "sad", "happy"] @=> string emotions[];
int emotionToNotes[2][20];
[60, 55, 64, 65, 67, 72] @=> emotionToNotes["happy"];
[60, 62, 63, 65, 67, 68] @=> emotionToNotes["sad"];

// <<< emotionToNotes["happy"][1] >>>; // 62

dur emotionToDurs[2];
0.25::second => emotionToDurs["happy"];
0.75::second => emotionToDurs["sad"];

emotions[1] => string curEmotion;



// music stuff

// modal bar for sound generation
//ModalBar bar => NRev nrev => Chorus chorus => dac;
ModalBar bar => NRev rev => dac;
4 => bar.preset;


// osc stuff (http://chuck.cs.princeton.edu/doc/examples/osc/OSC_recv.ck)

// create our OSC receiver
OscRecv recv;
// use port 12000
12000 => recv.port;
// start listening (launch thread)
recv.listen();

// create an address in the receiver, store in new variable
recv.event( "/wek/outputs, f" ) @=> OscEvent oe;



// do it!
spork ~ handleEmotions();
generateMusic();

fun void handleEmotions() {

    while (true) {
        <<< Math.random2(0,4) >>>;
        // listen to OSC
        // wait for event to arrive
        oe => now;

        // grab the next message from the queue. 
        if ( oe.nextMsg() != 0 )
        { 
            // getFloat fetches the expected int (as indicated by "i")
            oe.getFloat() $ int => int emotionIdx;
            // print
            <<< "got (via OSC):", emotionIdx >>>;
            emotions[emotionIdx] => curEmotion;

        }

        // set curEmotion
        <<< curEmotion >>>;
    }
}

fun void generateMusic() {
    while (true) {
        Math.random2(0, emotionToNotes[curEmotion].cap()-1) => int noteIdx; // TODO: randomize it
        emotionToNotes[curEmotion][noteIdx] => int note;
        emotionToDurs[curEmotion] => dur duration;
        Std.mtof(note) => float freq;
        (freq, duration, 0.75) => noteon;
    }
}

// strike the bar
fun void noteon(float f, dur len, float vel)
{
    f => bar.freq;

    Math.random2f(0.0, 0.25) => bar.strikePosition;
    Math.random2f(0.45, 0.5) => bar.stickHardness;
    Math.random2f(0.0, 0.1) => bar.damp;
    
    vel * 0.5 => bar.noteOn;
    len * 0.1 => now;
    0.0 => bar.noteOn;
    len * 0.9 => now;
    
    // 0.5 => bar.noteOn;
    
    <<< f, ", ", len >>>;
}
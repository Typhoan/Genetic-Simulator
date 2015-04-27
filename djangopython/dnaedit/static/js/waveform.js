 function generateWaveform(sequence) {
    "use strict";
    var list = [],
    i;
    alert("called waveform");
    for (i = 0; i < sequence.length; i += 1) {
        if (sequence.charAt(i) === "A") {
            list[list.length] = [(7 * i), 0.2, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            //list[list.length] = [(7 * i) + 1, 0.45, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            list[list.length] = [(7 * i) + 2, 0.7, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            list[list.length] = [(7 * i) + 3, 1 + ((Math.random() - 0.5) / 4), Math.random() / 10, Math.random() / 10, Math.random() / 10];
            list[list.length] = [(7 * i) + 4, 0.7, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            //list[list.length] = [(7 * i) + 5, 0.45, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            list[list.length] = [(7 * i) + 6, 0.2, Math.random() / 10, Math.random() / 10, Math.random() / 10];
        } else if (sequence.charAt(i) === "T") {
            list[list.length] = [(7 * i), Math.random() / 10, 0.2, Math.random() / 10, Math.random() / 10];
            //list[list.length] = [(7 * i) + 1, Math.random() / 10, 0.45, Math.random() / 10, Math.random() / 10];
            list[list.length] = [(7 * i) + 2, Math.random() / 10, 0.7, Math.random() / 10, Math.random() / 10];
            list[list.length] = [(7 * i) + 3, Math.random() / 10, 1 + ((Math.random() - 0.5) / 4), Math.random() / 10, Math.random() / 10];
            list[list.length] = [(7 * i) + 4, Math.random() / 10, 0.7, Math.random() / 10, Math.random() / 10];
            //list[list.length] = [(7 * i) + 5, Math.random() / 10, 0.45, Math.random() / 10, Math.random() / 10];
            list[list.length] = [(7 * i) + 6, Math.random() / 10, 0.2, Math.random() / 10, Math.random() / 10];
        } else if (sequence.charAt(i) === "G") {
            list[list.length] = [(7 * i), Math.random() / 10, Math.random() / 10, 0.2, Math.random() / 10];
            //list[list.length] = [(7 * i) + 1, Math.random() / 10, Math.random() / 10, 0.45, Math.random() / 10];
            list[list.length] = [(7 * i) + 2, Math.random() / 10, Math.random() / 10, 0.7, Math.random() / 10];
            list[list.length] = [(7 * i) + 3, Math.random() / 10, Math.random() / 10, 1 + ((Math.random() - 0.5) / 4), Math.random() / 10];
            list[list.length] = [(7 * i) + 4, Math.random() / 10, Math.random() / 10, 0.7, Math.random() / 10];
            //list[list.length] = [(7 * i) + 5, Math.random() / 10, Math.random() / 10, 0.45, Math.random() / 10];
            list[list.length] = [(7 * i) + 6, Math.random() / 10, Math.random() / 10, 0.2, Math.random() / 10];
        } else if (sequence.charAt(i) === "C") {
            list[list.length] = [(7 * i), Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.2];
            //list[list.length] = [(7 * i) + 1, Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.45];
            list[list.length] = [(7 * i) + 2, Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.7];
            list[list.length] = [(7 * i) + 3, Math.random() / 10, Math.random() / 10, Math.random() / 10, 1 + ((Math.random() - 0.5) / 4)];
            list[list.length] = [(7 * i) + 4, Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.7];
            //list[list.length] = [(7 * i) + 5, Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.45];
            list[list.length] = [(7 * i) + 6, Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.2];
        } else {
            //list[list.length] = [i, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            //list[list.length] = [i, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            list[list.length] = [i, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            list[list.length] = [i, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            list[list.length] = [i, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            list[list.length] = [i, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
            list[list.length] = [i, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
        }
    }
    return list;
}
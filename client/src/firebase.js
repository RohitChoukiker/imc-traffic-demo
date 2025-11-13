// firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// const firebaseConfig = {
//   apiKey: "AIzaSyDVyovmUsGl5u7ovIoJHSbq6TP-zWUCiKU",
//   authDomain: "instashare-b328c.firebaseapp.com",
//   projectId: "instashare-b328c",
//   storageBucket: "instashare-b328c.appspot.com",
//   messagingSenderId: "552445805110",
//   appId: "1:552445805110:web:833842421ea3ac1b8ece97",
// };


const firebaseConfig = {
  apiKey: "AIzaSyBb3eDNIHqveD0zCT51xKtzTrKElG-gxhQ",
  authDomain: "fir-c09cc.firebaseapp.com",
  projectId: "fir-c09cc",
  storageBucket: "fir-c09cc.firebasestorage.app",
  messagingSenderId: "807638259873",
  appId: "1:807638259873:web:5d2166a5c82649931638e0",
  measurementId: "G-YN2J8FJ30K"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

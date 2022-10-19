import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LandingPage from "./LandingPage";
import MainPage from "./MainPage";
import LoginPage from "./LoginPage";
import SignupPage from "./SignupPage";
import { Global } from "@emotion/react";
import { global } from "../styles/global";

const App = () => {
  return (
    <>
      <Global styles={global} />
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<LandingPage />} />
          <Route path="/mainPage" element={<MainPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;

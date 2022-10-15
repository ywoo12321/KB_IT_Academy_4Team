import styled from "@emotion/styled";
import theme from "../styles/theme";
import { useState } from "react";

const Navbar = () => {
  const [login, setLogin] = useState(false);

  return (
    <NavBox>
      <div className="navbar">
        <p>
          나만의
          <br />
          <span>감</span>성 <span>숙</span>소
        </p>
        <ul style={{ float: "right" }}>
          <li style={{ float: "left" }}>
            <button type="button">Search</button>
          </li>
          {!login && (
            <li style={{ float: "left" }}>
              <button type="button" onClick={() => setLogin(true)}>
                Log-in
              </button>
            </li>
          )}
          {login && (
            <li style={{ float: "left" }}>
              <button type="button" onClick={() => setLogin(false)}>
                Log-out
              </button>
            </li>
          )}
          {!login && (
            <li style={{ float: "left" }}>
              <button type="button">Sign-up</button>
            </li>
          )}
          {login && (
            <li style={{ float: "left" }}>
              <button type="button">My Page</button>
            </li>
          )}
        </ul>
      </div>
    </NavBox>
  );
};

export default Navbar;

const NavBox = styled.nav`
  & > div > p {
    float: left;
    display: inline;
    margin: 0;
    padding-left: 10px;
    color: ${theme.color.logoColor};
    font-family: ${theme.font_family.T};
    font-weight: 900;
    font-size: 27px;
    line-height: 111%;
    padding-top: 10px;
    padding-bottom: 10px;
    cursor: pointer;
  }
  & > div > p > span {
    color: ${theme.color.logoPointColor};
  }

  & > .navbar {
    width: 100%;
    height: 80px;
    background-color: ${theme.color.navColor};

    & > ul {
      margin: 0;
      list-style: none;
    }
    & > ul > li > button {
      line-height: 78px;
      float: right;
      margin-left: 26px;
      margin-right: 29px;
      border: none;
      background-color: ${theme.color.navColor};
      color: ${theme.color.whiteFont};
      font-family: ${theme.font_family.T};
      font-size: ${theme.font_size.h5};
      cursor: pointer;
    }
    & > ul > li > button:hover {
      color: ${theme.color.logoColor};
    }
  }
`;

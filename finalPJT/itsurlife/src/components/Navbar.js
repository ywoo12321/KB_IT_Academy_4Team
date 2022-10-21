import styled from "@emotion/styled";
import theme from "../styles/theme";
import { useState } from "react";
import { Link } from "react-router-dom";
import logo from "../images/logo.png";
import searchicon from "../images/searchicon.png";

const Navbar = () => {
  const [login, setLogin] = useState(false);

  return (
    <NavBox>
      <div className="navbar">
        <Link to="/mainPage" className="logolink">
          <img src={logo} alt="logo" />
        </Link>
        <div className="searchbox">
          <input type="text" placeholder="#모던 #경기도 등 원하는 검색어를 입력하세요." />
          <img src={searchicon} alt="searchicon" />
        </div>
        <ul style={{ float: "right" }}>
          {login && (
            <li style={{ float: "left" }}>
              <div id="toggle">
                <input type="checkbox" id="switch" />
                <label htmlFor="switch">Toggle</label>
              </div>
            </li>
          )}
          {!login && (
            <li style={{ float: "left" }}>
              <Link to="/login">
                <button className="btn" type="button">
                  Log-in
                </button>
              </Link>
            </li>
          )}
          {login && (
            <li style={{ float: "left" }}>
              <button className="btn" type="button" onClick={() => setLogin(false)}>
                Log-out
              </button>
            </li>
          )}
          {!login && (
            <li style={{ float: "left" }}>
              <Link to="/signup">
                <button className="btn" type="button">
                  Sign-up
                </button>
              </Link>
            </li>
          )}
          {login && (
            <li style={{ float: "left" }}>
              <button className="btn" type="button">
                My Page
              </button>
            </li>
          )}
        </ul>
      </div>
    </NavBox>
  );
};

export default Navbar;

const NavBox = styled.nav`
  & > .navbar > .searchbox {
    float: left;
    text-align: center;
    width: 530px;
    height: 60px;
    margin-left: 520px;
    margin-top: 10px;
    padding-right: 20px;
    border-radius: 40px;
    border: 2px solid ${theme.color.navColor};
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
  }
  & > div > .searchbox > input {
    display: inline;
    width: 92%;
    height: 50%;
    border: none;
    outline: none;
    margin-top: 14px;
    color: ${theme.color.main};
    font-family: ${theme.font_family.N};
    font-size: ${theme.font_size.h4};
  }
  & > div > .searchbox > input::placeholder {
    color: ${theme.color.gray};
    font-family: ${theme.font_family.N};
    font-size: ${theme.font_size.h5};
  }
  & > div > .searchbox > img {
    position: absolute;
    width: 30px;
    margin-top: 12px;
  }
  & > div > .logolink > img {
    float: left;
    display: flex;
    margin: 0;
    height: 80px;
    width: 120px;
    cursor: pointer;
  }
  & > div > p > span {
    color: ${theme.color.logoPointColor};
  }
  & > div {
    width: 95%;
    height: 80px;
    margin: auto;
    border-bottom: 3px solid ${theme.color.navColor};
  }
  & > div > ul {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  .btn {
    line-height: 78px;
    float: right;
    margin-left: 40px;
    border: none;
    color: ${theme.color.navColor};
    font-family: ${theme.font_family.T};
    font-size: ${theme.font_size.h5};
    cursor: pointer;
  }
  .btn:hover {
    color: ${theme.color.logoColor};
  }
  @media screen and (max-width: 768px) {
    .btn {
      margin-left: 6px;
      margin-right: 7px;
      font-size: ${theme.font_size.body1};
    }
    & > div > p {
      font-size: ${theme.font_size.subtitle1};
      line-height: 130%;
    }
  }

  #toggle {
    & > input[type="checkbox"] {
      height: 0;
      width: 0;
      visibility: hidden;
    }

    & > label {
      cursor: pointer;
      text-indent: -9999px;
      width: 100px;
      height: 50px;
      background: ${theme.color.navColor};
      display: block;
      border-radius: 100px;
      position: relative;
    }

    & > label:after {
      content: "";
      position: absolute;
      top: 2.5px;
      left: 2.5px;
      width: 45px;
      height: 45px;
      background: ${theme.color.whiteFont};
      border-radius: 90px;
      transition: 0.3s;
    }

    & > input:checked + label {
      background: ${theme.color.logoColor};
    }

    & > input:checked + label:after {
      left: calc(100% - 2.5px);
      transform: translateX(-100%);
    }

    & > label:active:after {
      width: 65px;
    }
  }
`;

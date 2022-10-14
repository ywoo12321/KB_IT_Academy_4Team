import styled from "@emotion/styled";
import theme from "../styles/theme";

const Navbar = () => {
  return (
    <NavBox>
      <div className="nav">
        <button type="button">
          나만의<br>감성숙소</br>
        </button>
        <button type="button">Search</button>
        <button type="button">Log-out</button>
        <button type="button">My Page</button>
      </div>
    </NavBox>
  );
};

export default Navbar;

const NavBox = styled.div`
  width: 100%;
  height: 80px;
  & > .nav {
    display: flex;
    align-items: center;
    background-color: ${theme.color.navbarColor};
    & > button {
      padding-left: 22px;
      color: ${theme.color.whiteFont};
      font-family: ${theme.font_family.T};
      font-size: ${theme.font_size.h5};
    }
  }
`;

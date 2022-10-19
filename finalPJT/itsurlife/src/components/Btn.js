import styled from "@emotion/styled";
import theme from "../styles/theme";

const Btn = ({ children, onclick }) => {
  return <Button onClick={onclick}>{children}</Button>;
};

export default Btn;

const Button = styled.button`
  width: 163px;
  height: 63px;

  background-color: ${theme.color.footerColor};
  border-radius: 30px;
  border: none;
  font-family: ${theme.font_family.N};
  font-size: ${theme.font_size.h4};
  line-height: 30px;

  text-align: center;

  :hover {
    background-color: ${theme.color.whiteFont};
    color: ${theme.color.footerColor};
    border: 3px solid ${theme.color.footerColor};
  }
`;

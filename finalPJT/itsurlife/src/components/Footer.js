import styled from "@emotion/styled";
import theme from "../styles/theme";

const Footer = () => {
  return (
    <FooterBox>
      <div className="foot">
        <p>
          주 소 : 서울특별시 강남구 언주로 508 14층(역삼동, 서울상록빌딩)
          <br />
          개발자 : 김영우, 박정우, 안선우, 이가은, 이원섭
          <br />
          Copyright by Multicampus Co., Ltd. All rights reserved.
        </p>
      </div>
    </FooterBox>
  );
};

export default Footer;

const FooterBox = styled.div`
  width: 100%;
  height: 80px;
  .foot {
    display: flex;
    align-items: center;
    background-color: ${theme.color.point};
  }

  & .foot > p {
    padding-left: 22px;
    color: ${theme.color.whiteFont};
    font-family: ${theme.font_family.N};
    font-size: ${theme.font_size.body2};
  }
`;

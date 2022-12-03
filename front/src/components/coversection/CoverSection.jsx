import styles from './CoverSection.module.scss';
import bg1 from '../../static/bg1.jpeg';
import bg2 from '../../static/bg2.jpeg';
import bg3 from '../../static/bg3.jpeg';
import Carousel from 'react-bootstrap/Carousel';
import {RiPlantLine} from 'react-icons/ri';
import {useTranslation} from 'react-i18next';

const CoverSection = () => {
    const {t} = useTranslation();

    return (
        <Carousel>
            <Carousel.Item>
                <img className={styles.image} src={bg1} alt="First slide"/>
                <Carousel.Caption className={styles.textwrapper}>
                    <h3 className={styles.maintext}><RiPlantLine/> Laplanta</h3>
                    <p className={styles.additionaltext}>{t("cover_1")}</p>
                </Carousel.Caption>
            </Carousel.Item>
            <Carousel.Item>
                <img className={styles.image} src={bg2} alt="First slide"/>
                <Carousel.Caption className={styles.textwrapper}>
                    <h3 className={styles.maintext}><RiPlantLine/> Laplanta</h3>
                    <p className={styles.additionaltext}>{t("cover_2")}</p>
                </Carousel.Caption>
            </Carousel.Item>
            <Carousel.Item>
                <img className={styles.image} src={bg3} alt="First slide"/>
                <Carousel.Caption className={styles.textwrapper}>
                    <h3 className={styles.maintext}><RiPlantLine/> Laplanta</h3>
                    <p className={styles.additionaltext}>{t("cover_3")}</p>
                </Carousel.Caption>
            </Carousel.Item>
        </Carousel>
    );    
}

export default CoverSection;
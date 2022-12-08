import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import styles from './Missing.module.scss';
import {TbMoodCry} from 'react-icons/tb';
import Button from 'react-bootstrap/Button';
import {Link} from 'react-router-dom';
import {useTranslation} from 'react-i18next';

const Missing = () => {
    const {t} = useTranslation();

    return (
        <Container className={styles.wrapper}>
            <Row>
                <Col>
                    <TbMoodCry className="text-light" size={500}/>
                </Col>
                <Col>
                    <Container className={styles.container}>
                        <h1 className='text-light' style={{fontSize: '10rem'}}>{t("oops")}</h1>
                        <h5 className='text-light'>{t("page_not_found")}</h5>
                    </Container>
                </Col>
            </Row>
            <Row>
                <Col className={styles.button}>
                    <Button variant="outline-light">
                        <Link to='/' className='text-light' style={{textDecoration: 'none'}}>{t("go_home")}</Link>
                    </Button>
                </Col>
            </Row>
        </Container>
    );
}

export default Missing;
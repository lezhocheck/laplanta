import React from 'react';
import Accordion from 'react-bootstrap/Accordion';
import styles from './Blog.module.scss';
import {useTranslation} from 'react-i18next';

const Blog = () => {
    const {t} = useTranslation();

    return (
        <div className={styles.wrapper}>
            <Accordion className={styles.accordion} flush defaultActiveKey="0">
                <Accordion.Item eventKey="0">
                    <Accordion.Header>{t("blog_quest_1")}</Accordion.Header>
                    <Accordion.Body>
                        {t("blog_desc")}
                    </Accordion.Body>
                </Accordion.Item>
                <Accordion.Item eventKey="1">
                    <Accordion.Header>{t("blog_quest_2")}</Accordion.Header>
                    <Accordion.Body>
                        {t("blog_desc")}
                    </Accordion.Body>
                </Accordion.Item>
                <Accordion.Item eventKey="2">
                    <Accordion.Header>{t("blog_quest_3")}</Accordion.Header>
                    <Accordion.Body>
                        {t("blog_desc")}
                    </Accordion.Body>
                </Accordion.Item>
            </Accordion>
        </div>
    );
}

export default Blog;
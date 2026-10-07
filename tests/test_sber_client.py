from app.services.sber_client import SberVacancy


def test_sber_vacancy_parses_external_camel_case_contract() -> None:
    item = SberVacancy.model_validate(
        {
            "requisitionId": "5062b4e1-07a9-4100-b35e-3cb825ccc0d4",
            "title": "ML Engineer",
            "company": "ПАО Сбербанк",
            "publicationDate": "2026-10-07T15:28:41.000Z",
            "city": "г Москва",
            "unknownField": "ignored",
        }
    )

    assert item.requisition_id == "5062b4e1-07a9-4100-b35e-3cb825ccc0d4"
    assert item.publication_date is not None
    assert item.city == "г Москва"

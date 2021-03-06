__author__ = 'sweemeng'
from rest_framework import status
from popit.signals.handlers import *
from popit.models import *
import logging
from django.conf import settings
from popit.tests.base_testcase import BasePopitAPITestCase


class PostAPITestCase(BasePopitAPITestCase):

    def test_view_post_list(self):

        response = self.client.get("/en/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("page" in response.data)
        self.assertEqual(response.data["per_page"], settings.REST_FRAMEWORK["PAGE_SIZE"])

    def test_view_post_detail_not_exist_unauthorized(self):
        response = self.client.get("/en/posts/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_post_detail_not_exist_authorized(self):
        response = self.client.get("/en/posts/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_post_detail_exist_unauthorized(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("memberships" in response.data["result"])


    def test_view_post_detail_exist_authorized(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_unauthorized(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
            "start_date": "2000-2-2",
            "end_date": "2030-2-2",
        }
        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_authorized(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
            "start_date": "2000-02-02",
            "end_date": "2030-02-02",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.language("en").get(role="Honorary Member")
        self.assertEqual(post.organization_id, "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")

    def test_update_post_unauthorized(self):
        data = {
            "label": "member"
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_not_exist_unauthorized(self):
        data = {
            "label": "member"
        }
        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_authorized(self):
        data = {
            "label": "member"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        self.assertEqual(post.label, "member")

    def test_update_post_not_exist_authorized(self):
        data = {
            "label": "member"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_unauthorized(self):
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_not_exist_unauthorized(self):
        response = self.client.delete("/en/posts/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete("/en/posts/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_post_otherlabels_not_exist_unauthorized(self):
        data = {
            "other_labels": [{
                "name": "sampan party"
            }]
        }

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_otherlabels_not_exist_authorized(self):
        data = {
            "other_labels": [{
                "name": "sampan party"
            }]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_post_otherlabels_exist_unauthorized(self):
        data = {
            "other_labels": [{
                "name": "sampan party"
            }]
        }

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_otherlabels_exist_authorized(self):
        data = {
            "other_labels": [{
                "name": "sampan party"
            }]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_otherlabels_not_exist_unauthorized(self):
        data = {
            "other_labels": [
                {
                    "id":"aee39ddd-6785-4a36-9781-8e745c6359b7",
                    "name": "Bilge Rat"
                }
            ]
        }
        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_otherlabels_not_exist_authorized(self):
        data = {
            "other_labels": [
                {
                    "id":"aee39ddd-6785-4a36-9781-8e745c6359b7",
                    "name": "Bilge Rat"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_otherlabels_exist_unauthorized(self):
        data = {
            "other_labels": [
                {
                    "id":"aee39ddd-6785-4a36-9781-8e745c6359b7",
                    "name": "Bilge Rat"
                }
            ]
        }

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_otherlabels_exist_authorized(self):
        data = {
            "other_labels": [
                {
                    "id":"aee39ddd-6785-4a36-9781-8e745c6359b7",
                    "name": "Bilge Rat"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_contacts_not_exist_unauthorized(self):
        data = {
            "contact_details": [
                {
                    "type": "sms",
                    "value": "231313123131",
                }
            ]
        }

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_contacts_not_exist_authorized(self):
        data = {
            "contact_details": [
                {
                    "type": "sms",
                    "value": "231313123131",
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_post_contacts_exist_unauthorized(self):
        data = {
            "contact_details": [
                {
                    "type": "sms",
                    "value": "231313123131",
                }
            ]
        }

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_contacts_exist_authorized(self):
        data = {
            "contact_details": [
                {
                    "type": "sms",
                    "value": "231313123131",
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_contacts_not_exist_unauthorized(self):
        data = {
            "contact_details": [
                {
                    "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
                    "type": "phone"
                }
            ]
        }

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_contacts_not_exist_authorized(self):
        data = {
            "contact_details": [
                {
                    "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
                    "type": "phone"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_contacts_exist_unauthorized(self):
        data = {
            "contact_details": [
                {
                    "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
                    "type": "phone"
                }
            ]
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_contacts_exist_authorized(self):
        data = {
            "contact_details": [
                {
                    "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
                    "type": "phone"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_links_not_exist_unauthorized(self):
        data = {
            "links": [
                {
                    "url": "http://www.yahoo.com"
                }
            ]
        }

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_links_not_exist_authorized(self):
        data = {
            "links": [
                {
                    "url": "http://www.yahoo.com"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_post_links_exist_unauthorized(self):
        data = {
            "links": [
                {
                    "url": "http://www.yahoo.com"
                }
            ]
        }

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_links_exist_authorized(self):
        data = {
            "links": [
                {
                    "url": "http://www.yahoo.com"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_links_not_exist_unauthorized(self):
        data = {
            "links": [
                {
                    "id": "ce15a9ee-6742-4467-bbfb-c86459ee685b",
                    "note": "just a link"
                }
            ]
        }

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_links_not_exist_authorized(self):
        data = {
            "links": [
                {
                    "id": "ce15a9ee-6742-4467-bbfb-c86459ee685b",
                    "note": "just a link"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_links_exist_unauthorized(self):
        data = {
            "links": [
                {
                    "id": "ce15a9ee-6742-4467-bbfb-c86459ee685b",
                    "note": "just a link"
                }
            ]
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_links_exist_authorized(self):
        data = {
            "links": [
                {
                    "id": "ce15a9ee-6742-4467-bbfb-c86459ee685b",
                    "note": "just a link"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_post_translated_nested(self):
        response = self.client.get("/ms/posts/2c6982c2-504a-4e0d-8949-dade5f9e494e/")
        results = response.data["result"]
        self.assertEqual(results["organization"]["name"], "Parti Lanun KL")
        self.assertEqual(results["organization"]["language_code"], "ms")

    def test_fetch_post_translated(self):
        response = self.client.get("/ms/posts/2c6982c2-504a-4e0d-8949-dade5f9e494e/")
        results = response.data["result"]
        self.assertEqual(results["label"], "kapten parti lanun KL")
        self.assertEqual(results["language_code"], "ms")

    def test_create_post_invalid_date(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
            "start_date": "invalid date",
            "end_date": "invalid date",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_create_post_api_role_more_20_char(self):
        data = {
            "result": {

                "html_url": "https://sinar-malaysia.popit.mysociety.org/posts/545f7f5d5222837c2c05b740",
                "url": "https://sinar-malaysia.popit.mysociety.org/api/v0.1/posts/545f7f5d5222837c2c05b740",
                "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3", # Actual ID in production 545e01f45222837c2c0586f3
                "area": {
                        "state": "Kelantan",
                        "id": "N1",
                        "name": "Pengkalan Kubor"
                },
                "role": "Member of State Assembly",
                "label": "ADUN for Pengkalan Kubor",
                "id": "545f7f5d5222837c2c05b740",
                "images": [ ],
                "memberships": [ ],
                "links": [ ],
                "contact_details": [ ]
            }

        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/posts/", data["result"])
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_api_invalid_organization(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "not exist",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_create_post_api_invalid_area(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "not exist",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_create_post_api_no_organization(self):
        data = {
            "label": "Honorary Member",
            "role": "Honorary Member",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_api_translated(self):
        data = {
            "label": "Ahli Terhormat",
            "role": "Ahli Terhormat",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/ms/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        logging.warn(response.data)
        self.assertEqual(response.data["result"]["label"], "Ahli Terhormat")
        self.assertEqual(response.data["result"]["role"], "Ahli Terhormat")

    def test_update_post_api_translated(self):
        data = {
            "label": "ahli"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/ms/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post = Post.objects.language("ms").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        self.assertEqual(post.label, "ahli")

    def test_create_post_api_with_membership(self):
        data = {
            "label": "parrot of pirate party",
            "memberships": [
                {
                    "label": "test membership",
                    "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
                    "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_post_blank_id_authorized(self):
        data = {
            "id": "",
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
            "start_date": "2000-02-02",
            "end_date": "2030-02-02",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.language("en").get(role="Honorary Member")
        self.assertEqual(post.organization_id, "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
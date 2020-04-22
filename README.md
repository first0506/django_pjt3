# READEME

### 구현과정

* 로그인 하기 전, 기존 URL이 함께 넘어왔다면 해당 URL로 이동하도록 

```python
def login(request):
    if request.user.is_authenticated:
        return redirect('community:index')
    if request.method=='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'community:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)
```

과 같이 설계했다. 하지만 몇몇 기능에서 작동하지 않았다.

로그인 전 정보가 `GET`방식으로 넘어오다보니 `POST`방식만 사용해야 하는 몇몇 기능에서 작동하지 않았다. 예를 들어, 

```python
@require_POST
def comments_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
    return redirect('community:detail', review.pk)
```

와 같이 댓글을 생성할 때는 form에서 POST방식으로 불러왔기 때문에 로그아웃 상태에서 썼던 댓글이 로그인 후에는 사라진 것을 확인할 수 있었다. 그래서 해당 기능들은 templates에서 로그인 전에는 기능이 활성화되지 않도록 조치시켰다.

```html
{% if user.is_authenticated %}
<a href="{% url 'community:update' review.pk %}">수정하기</a>
{% else %}
    <p>수정은 로그인이 필요합니다.</p>
{% endif %}


{% if user.is_authenticated %}
    <form action="{% url 'community:comments_create' review.pk %}" method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button>댓글작성</button>
    </form>
{% else %}
    <p>댓글은 로그인이 필요합니다.</p>
{% endif %}
```



### 페어프로그래밍 느낀점

우선 처음으로 페어프로그래밍을 진행했는데 내가 보지 못했던 부분들을 상대방이 알려주어서 프로젝트가 일찍 

끝날 수 있게 되었다. 특히 에러가 나거나 구현이 잘 안되는 기능에 대해서 서로 토의해 가면서 기능을 결국 구현했

을 때 페어프로그래밍의 진면목을 느낄 수 있었다. 아직은 서툰 부분이 많아서 서로 헷갈리기도 하고, 변수 선정에

도 애를 먹었지만 이는 차츰 페어프로그래밍을 진행하면서 익숙해질 부분인 것 같다.
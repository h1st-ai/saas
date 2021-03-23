resource "aws_route53_zone" "cn" {
  name = "cn.h1st.ai"
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.cn.zone_id
  name    = "staging.cn.h1st.ai"
  type    = "A"
  ttl     = "300"
  records = [aws_eip.workbench.public_ip]
}
